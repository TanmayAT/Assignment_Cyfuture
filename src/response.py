import google.generativeai as genai
import inspect
import json
import re
import datetime  
from .tools import tools  
from .prompt import Conversational_Prompt , Tool_Prompt


api_key = "AIzaSyCqqXochDTlqutMHKjcVHc87hLdmOKoju0"
genai.configure(api_key=api_key)


def context_function(request_id: int, chat_store: dict = None):
    history = chat_store.get(request_id, [])
    return "\n".join([f"User: {u}\nBot: {b}" for u, b in history])


def model_function(user_query, context: str):
    prompt = Conversational_Prompt
    req = f"{prompt}\n\n{context}\n\nUser: {user_query}\nBot:"
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(req)
    return response.text.strip()


def clean_json_string(json_string: str) -> str:
    """
    Cleans the LLM response by removing markdown formatting like triple backticks and extra whitespace.
    """
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", json_string.strip(), flags=re.IGNORECASE)
    return cleaned.strip()

def parse_tool_call(output: dict):
    try:
        return output.get("tool"), output
    except Exception as e:
        print(f"[Parse Error]: {e}")
        return None, None

def default_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return str(obj)

async def smart_model_handler(user_query, request_id=0, chat_store=None):

    print(f"[User Query]: {user_query}")

    tool_decider_prompt = Tool_Prompt
    model = genai.GenerativeModel("gemini-2.0-flash")

    try:
        tool_response = model.generate_content(tool_decider_prompt)
        print(f"[Tool Response]: {tool_response.text}")
        clean_resp = clean_json_string(tool_response.text)
        parsed = json.loads(clean_resp)
    except Exception as e:
        print(f"[Tool JSON Parse Failed]: {e}")
        parsed = {"tool": "none"}

    tool_name = parsed.get("tool", "none")

    # Step 2: No tool → fallback to chat
    if tool_name == "none":
        context = context_function(request_id, chat_store)
        reply = model_function(user_query, context)
        if chat_store is not None:
            chat_store.setdefault(request_id, []).append((user_query, reply))
        return reply

    # Step 3: Tool call
    tool = next((t for t in tools if t.name == tool_name), None)
    if not tool:
        return f" Tool '{tool_name}' not found."

    try:
        sig = inspect.signature(tool.func)
        tool_args = {k: v for k, v in parsed.items() if k in sig.parameters}

        print(f"[Calling Tool]: {tool_name} with args {tool_args}")

        if inspect.iscoroutinefunction(tool.func):
            result = await tool.func(**tool_args)
        else:
            result = tool.func(**tool_args)

        result_str = result if isinstance(result, str) else json.dumps(result, indent=2, default=default_serializer)

        if chat_store is not None:
            chat_store.setdefault(request_id, []).append((user_query, result_str))

        return result_str

    except Exception as e:
        return f" Tool execution failed: {e}"
