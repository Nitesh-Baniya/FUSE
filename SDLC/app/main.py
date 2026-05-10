from fastapi import FastAPI
from app.router import router
from app.logger import logger
from app.database import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Customer API",
    description="A RESTful API for managing customer data",
    version="1.0.0"
)

# Include the customer router
app.include_router(router, prefix="/api/v1", tags=["customers"])

@app.get("/")
def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return {"message": "Customer API is running", "docs": "/docs", "version": "1.0.0"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "Customer API"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application")
    uvicorn.run(app, host="0.0.0.0", port=8000)