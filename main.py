import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables for local testing
load_dotenv()

app = FastAPI(
    title="East Coast E-Bike Warranty & Repair Hub",
    description="Backend logic for Bafang regional diagnostics and warranty claims.",
    version="1.0.0"
)

# --- CORS CONFIGURATION ---
# This allows your React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SUPABASE SETUP ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("WARNING: Supabase credentials missing. Check your environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- ROUTES ---

@app.get("/")
async def health_check():
    return {
        "status": "online",
        "hub": "East Coast E-Bike Warranty Center",
        "location": "Alliance, Ohio",
        "partner": "Bafang Regional Service"
    }

@app.get("/bo/diagnose/{error_code}")
async def get_bo_advice(error_code: int):
    """
    Fetches technical fix advice from the Bafang Dealer Manual data
    stored in the manufacturer_specs table.
    """
    try:
        response = supabase.table("manufacturer_specs") \
            .select("fix_advice") \
            .eq("error_code", error_code) \
            .eq("brand", "Bafang") \
            .execute()
        
        if not response.data:
            return {
                "bo_says": f"I don't have a specific fix for Error {error_code} in my database yet, Mike. Check the hardware continuity.",
                "status": "not_found"
            }
        
        return {
            "error_code": error_code,
            "bo_says": response.data[0]['fix_advice'],
            "source": "Bafang Dealer Manual"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/claims/new")
async def create_claim(claim: dict):
    """
    Submits a new warranty claim. 
    Differentiates between 'retail' (direct) and 'partner_shop' (B2B).
    """
    try:
        # Default to retail if not specified
        if "claim_source" not in claim:
            claim["claim_source"] = "retail"
            
        result = supabase.table("claims").insert(claim).execute()
        return {"message": "Claim successfully logged", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to log claim: {str(e)}")

@app.get("/inventory/bafang-parts")
async def get_parts():
    """
    Quick check for common Bafang rebuild components (controllers, hall sensors, nylon gears).
    """
    try:
        result = supabase.table("inventory").select("*").eq("category", "Bafang").execute()
        return {"inventory": result.data}
    except Exception as e:
        return {"error": "Could n't inventory:"}
        
