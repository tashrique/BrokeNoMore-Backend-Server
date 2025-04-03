from fastapi import FastAPI
from app.api.api import api_router
from app.db.supabase_client import get_supabase_client
import uvicorn
from app.core.config import settings
app = FastAPI(
    title="BrokeNoMore",
    description="BrokeNoMore is a platform for people to get help when they are in need.",
    version="0.1.0",
)

# Initialize database connection
get_supabase_client()

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "BrokeNoMore Server is running. Check out the docs at /docs"}


@app.get("/health")
async def health():
    return {"message": "BrokeNoMore Server is running."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
