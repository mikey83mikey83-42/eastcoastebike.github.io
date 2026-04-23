from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os

# --- THIS IS THE VARIABLE RENDER IS LOOKING FOR ---
app = FastAPI(title="East Coast E-Bike Tech Hub")

# CORS Setup - Allows your GitHub Pages site to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, you can change this to your specific GitHub URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Credentials (Ensure these are set in Render's Environment Variables)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Only initialize if keys exist to prevent crashing on build
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("WARNING: Supabase credentials missing!")

# Data model for Bafang diagnostics
class Diagnostic(BaseModel):
    serial_number: str
    firmware_ver: str
    error_codes: list
    mileage: int

@app.get("/")
def read_root():
    return {"status": "Online", "service": "East Coast E-Bike API"}

@app.post("/sync")
async def sync_data(data: Diagnostic):
    try:
        response = supabase.table("motor_logs").insert({
            "serial_number": data.serial_number,
            "firmware_ver": data.firmware_ver,
            "errors": data.error_codes,
            "mileage": data.mileage
        }).execute()
        return {"status": "Success", "id": response.data[0]['id']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# This block ensures it runs correctly if you test it locally
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    import os
from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI()

# Connect to your new "Memory"
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.get("/")
async def root():
    return {"status": "Online", "service": "East Coast E-Bike API", "database": "Connected"}

# This will handle your automated shipping logic later
@app.post("/add-shipping")
async def add_shipping(tracking: str, carrier: str):
    data = {"tracking_number": tracking, "carrier": carrier}
    response = supabase.table("shipping_logs").insert(data).execute()
    return {"message": "Shipping record saved!", "data": response.data}

# This will be where we trigger those cool AI visuals
@app.post("/generate-art")
async def generate_art(prompt: str):
    # We will plug the AI generation code here next!
    return {"message": f"Ready to generate visual for: {prompt}"}
    
