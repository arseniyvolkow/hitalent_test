import logging
from fastapi import FastAPI
from app.api.endpoints import departments

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Organizational Structure API")

app.include_router(departments.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Organizational Structure API"}
