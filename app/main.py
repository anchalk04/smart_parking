import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Create a FastAPI application instance
app = FastAPI()

# Import the routers for your different modules.
from app.auth import router as auth_router
from app.parking_slots import router as parking_router

# Include the routers to add their endpoints to the main application.
# The auth_router now handles all authentication endpoints.
app.include_router(auth_router)

# The parking_router handles all parking-related endpoints.
app.include_router(parking_router)

# You can add a simple root endpoint for a health check
@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Parking Backend API!"}