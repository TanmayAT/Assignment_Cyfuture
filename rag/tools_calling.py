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

    data = MongoConnector.get_complaint_by_id()

    phone_number = data.get("Phone_Number", "N/A")
    name = data.get("Name", "N/A")
    application_status = data.get("Application_Status", "N/A")
    complaint_details = data.get("Complaint_Details", "N/A")

    
    return {

        "Phone_Number" : phone_number, 
        "Name" : name , 
        "Application_Status" : application_status,
        "Complaint_Details" : complaint_details
        
    }