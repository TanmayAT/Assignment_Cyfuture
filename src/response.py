import google.generativeai as genai
from .prompt import Prompt


api_key = "AIzaSyCqqXochDTlqutMHKjcVHc87hLdmOKoju0"
genai.configure(api_key=api_key)


def context_function(request_id: int , chat_store: dict = None):
    history = chat_store.get(request_id, [])
    context = ""
    for i, (user_msg, bot_reply) in enumerate(history, 1):
        context += f"\nUser: {user_msg}\nBot: {bot_reply}"
    return context


def model_function(user_query, context: str):
    prompt = Prompt
    req = f"{prompt}\n\n{context}\n\nUser: {user_query}\nBot:"

    model = genai.GenerativeModel("gemini-2.0-flash")  
    response = model.generate_content(req)  

    return response.text.strip()
