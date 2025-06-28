from mcp.server.fastmcp import FastMCP
import logging
from .connector import MongoConnector
from fastapi.exceptions import HTTPException
from pydantic import EmailStr


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Query_resolver")

# Initialize MCP server
mcp = FastMCP("querry-resolver")

# Initialize MongoDB connector
db = MongoConnector("mongodb+srv://vaidikpandeytt:JJEmTHNTyFgGPnjq@communicationdb.4zlwhdh.mongodb.net/?retryWrites=true&w=majority&appName=Communicationdb")


# ---------------------- MCP Tools ---------------------- #

@mcp.tool(
    name="update_check",
    description="Get the current Updated Status from the database ."
)

async def update_check(complaint_id: str):
    logger.debug(f"Received complaint_id: {complaint_id}")
    result = db.get_complaint_by_id(complaint_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result

@mcp.tool(
        name = "Create_complaint",
        description="Pushing compalints in db"
)
def Create_complaint(name: str, phone_number: str, email: EmailStr, complaint_details: str):
    return db.create_complaint(
        name=name,
        phone_number=phone_number,
        email=email,
        complaint_details=complaint_details
    )

