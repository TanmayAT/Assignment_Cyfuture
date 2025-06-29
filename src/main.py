from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from .response import smart_model_handler  

# Configure logging
logging.basicConfig(filename="/app/app.log" ,level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
builder = FastAPI()

# Chat store to maintain context
chat_store = {}

# Middleware for logging
@builder.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    logger.debug(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.debug(f"Response status: {response.status_code}")
    return response

# Health check
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

        query = body.get("query", "").strip()
        if not query:
            
            return JSONResponse(content={"error": "No query provided"}, status_code=400)

        logger.debug(f"[request_id: {request_id}] Query: {query}")

        
        reply = await smart_model_handler(query, request_id, chat_store)

        # ✅ Save conversation in context
        chat_store.setdefault(request_id, []).append((query, reply))

        return JSONResponse(content={"response": reply}, status_code=200)

    except Exception as e:
        logger.exception("Exception during /communicate")
        return JSONResponse(content={"error": str(e)}, status_code=500)
