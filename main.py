import os
from fastapi import FastAPI
from square.client import Client

# Ensure the filename is Main.py for Render
app = FastAPI()

# Retrieve your Square Access Token from environment variables
# Remember to set SQUARE_ACCESS_TOKEN in your Render Dashboard
access_token = os.environ.get('SQUARE_ACCESS_TOKEN')

# Initialize the Square Client
# Using the environment variable directly to avoid AttributeError
client = Client(
    access_token=access_token,
    environment='sandbox'  # Change to 'production' when you are ready to go live
)

@app.get("/")
def read_root():
    return {
        "status": "success", 
        "message": "FastAPI is running with Square Integration"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Example Square API call structure
@app.get("/locations")
def list_locations():
    result = client.locations.list_locations()
    if result.is_success():
        return result.body
    elif result.is_error():
        return {"error": result.errors}
        
