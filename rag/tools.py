from langchain_community.tools import Tool 
from .tools_calling import update_check_tool



# LangChain Tool Integration





tools = [
    Tool(
        name="update_check",
        func=update_check_tool,
        description="Get the current Status of Applications"
    )
]