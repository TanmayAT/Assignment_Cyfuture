from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse 
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr
import logging
from .response import model_function, context_function
from .connector import MongoConnector


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

builder = FastAPI()
db = MongoConnector("mongodb+srv://vaidikpandeytt:JJEmTHNTyFgGPnjq@communicationdb.4zlwhdh.mongodb.net/?retryWrites=true&w=majority&appName=Communicationdb")

# Global chat store 
chat_store = {}


class ComplaintInput(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    complaint_details: str

@builder.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    logger.debug(f"Request: {request.method} & {request.url}")
    response = await call_next(request)
    logger.debug(f"Response: {response.status_code}")
    return response

@builder.get("/")
async def root():
    return {"message": "Entrypoint is ready to be exposed"}

@builder.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)

@builder.post("/communicate")
async def communicate(request: Request, request_id: int):
    try:
        body = await request.json()
        logger.debug(f"Received body: {body}")

        query = body.get("query", "")
        logger.debug(f"Received query: {query}")
        logger.debug(f"Received request_id (from param): {request_id}")

        if not query:
            return JSONResponse(content={"error": "No query provided"}, status_code=400)

        context = context_function(request_id, chat_store)
        reply = model_function(query, context)

        chat_store.setdefault(request_id, []).append((query, reply))

        return JSONResponse(content={"response": reply}, status_code=200)

    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)



@builder.post("/complaints")
def create_complaint(data: ComplaintInput):
    return db.create_complaint(**data.dict())

@builder.get("/complaints/{complaint_id}")
def get_complaint(complaint_id: str):
    result = db.get_complaint_by_id(complaint_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result