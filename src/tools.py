from langchain_community.tools import Tool 
from .tools_calling import update_check , Create_complaint



# LangChain Tool Integration

tools = [
    Tool(
        name="update_check",
        func= update_check,
        description="Get the current Status of Applications"
    ),
    Tool(
        name = "Create_complaint",
        func = Create_complaint,
        description = "Create complaints and push in db"

    )
]