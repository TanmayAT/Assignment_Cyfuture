import json
import inspect
import asyncio
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools import tools  # Ensure this module is correctly implemented

# Set your Google API Key (ensure this is set securely in production)
os.environ["GOOGLE_API_KEY"] = "AIzaSyCqqXochDTlqutMHKjcVHc87hLdmOKoju0"

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

agent_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are a helpful assistant. Based on the query, decide which tool to use from the following options:
1. get_stock_price - To get stock prices for a given ticker symbol.
2. get_company_facts - To get company facts for a given ticker symbol.
3. WebSearch - To search the web for the latest information.

Provide only the name of the tool to use, along with any required arguments in valid JSON format.

Your entire response MUST be valid JSON.
Don't give any '''{{}}''' or ```json or ``` — these are highly penalized.

Example:
{{
  "tool": "get_stock_price",
  "ticker": "AAPL",
  "query": "What is the stock price of Apple?"
}}

Json Schema:
{{
  "tool": "string",
  "ticker": "string",
  "query": "string"
}}

Output:
1. Only strict JSON format.
2. Do not include any other text or explanation.
3. Do not include any other information.

query: {query}
"""
)


# Create the LLMChain
llm_chain = agent_prompt | llm


def clean_json_string(json_string: str) -> str:

    """
    Cleans the JSON string by removing unwanted characters.
    """
    # Remove any leading/trailing whitespace and unwanted characters
    cleaned_string = json_string.strip("```json").strip("```").strip()

    return cleaned_string

# Function to parse the tool output safely
def parse_tool_call(output:dict):
    try:
       

        return output.get("tool"), output
    
    except Exception as e:
        print(f"[Parse Error]: {e}")
        return None, None
# Main agent logic
async def call_agent(query: str):
    print(f"[User Query]: {query}")
    
    try:
        agent_output = llm_chain.invoke({"query": query})
        print(f"[Agent Output]: {agent_output}")

    except Exception as e:
        print(f"[LLM Invocation Error]: {e}")
        return "Failed to generate a response from the language model."

    print(f"[LLM Output]: {agent_output}")

    # Parse the tool output
    agent_output.content = clean_json_string(agent_output.content)
    print(f"[Cleaned Agent Output]: {agent_output.content}")

    tool_name, tool_args = parse_tool_call(json.loads(agent_output.content))

    if not tool_name:
        return "Failed to parse tool output."

    # Look for the correct tool based on its name
    tool = next((tool for tool in tools if tool.name == tool_name), None)
    if not tool:
        return f"Tool '{tool_name}' not found."

    try:
        # Filter arguments based on the tool's function signature
        sig = inspect.signature(tool.func)
        filtered_args = {k: v for k, v in tool_args.items() if k in sig.parameters}

        # Execute the tool function asynchronously if it's a coroutine
        if inspect.iscoroutinefunction(tool.func):
            result = await tool.func(**filtered_args)
        else:
            result = tool.func(**filtered_args)

        # Handle the result based on its type (dictionary or string)
        if isinstance(result, dict):
            if "error" in result:
                return f"Error: {result['error']}"
            elif "price" in result:
                return f"{result['ticker']} is trading at {result['price']} {result['currency']}"
        else:
            return result 

    except Exception as e:
        
        return f"Error calling tool '{tool_name}': {e}"