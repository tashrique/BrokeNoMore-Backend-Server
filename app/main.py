from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import settings and database
from app.core.config import settings
from app.db.base import Base, engine
from app.db.init_db import init_db

# Import API router
from app.api.api import api_router

# Initialize the database (create tables)
init_db()

# Create FastAPI app
app = FastAPI(
    title="BrokeNoMore API",
    description="AI Financial Advisor for College Students",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to BrokeNoMore API - AI Financial Advisor for College Students",
        "docs": "/docs",
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 