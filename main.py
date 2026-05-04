import os
from fastapi import FastAPI
from square.client import Client

app = FastAPI()

# Configuration for Production
# Ensure you have 'SQUARE_ACCESS_TOKEN' set in your Render environment variables
client = Client(
    access_token=os.environ.get('SQUARE_ACCESS_TOKEN'),
    environment='production' 
)

@app.get("/")
async def root():
    return {"status": "active", "service": "E-Bike Warranty & Repair Hub"}

@app.get("/test-connection")
async def test_connection():
    # Simple call to verify the token and production connection
    result = client.locations.list_locations()
    
    if result.is_success():
        return {"status": "Connected to Square", "locations": result.body}
    else:
        return {"status": "Connection Failed", "errors": result.errors}

if __name__ == "__main__":
    import uvicorn
    # Render automatically assigns a PORT; defaults to 10000 if not found
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
