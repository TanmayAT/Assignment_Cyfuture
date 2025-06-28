from langchain_community.tools import Tool 
from .tools_calling import web_search_tool , get_stock_price_tool , get_company_facts_tool
# LangChain Tool Integration
tools = [
    Tool(
        name="get_stock_price",
        func=get_stock_price_tool,
        description="Get the current stock price for a given ticker symbol."
    ),
    Tool(
        name="get_company_facts",
        func=get_company_facts_tool,
        description="Get company facts for a given ticker symbol."
    ),
    Tool(
        name="WebSearch",
        func=web_search_tool,
        description="Search the web for a given query."
    )
]