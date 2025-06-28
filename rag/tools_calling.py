from mcp.server.fastmcp import FastMCP
import logging
from ..src.connector import MongoConnector

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("financial-datasets-mcp")

# Initialize MCP server
mcp = FastMCP("querry-resolver")


# ---------------------- MCP Tools ---------------------- #

@mcp.tool(
    name="update_cheack",
    description="Get the current Updated Status from the database ."
)


def update_check_tool():

    MongoConnector.get_complaint_by_id(id)

    


    return {

        "Phone_Number" : 
        "Name" : 
        "Application_Status" : 
        "Complaint_Details" :
        
    }