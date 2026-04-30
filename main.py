import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="East Coast E-Bike Warranty Hub")

# Supabase Setup
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.get("/")
async def root():
    return {"status": "East Coast Hub is Live", "service": "Bafang Regional Hub"}

# Bo's AI Diagnostic Helper
@app.get("/bo/diagnose/{error_code}")
async def get_diagnostic(error_code: int):
    # Pulls the tech data we inserted via the migration
    response = supabase.table("manufacturer_specs") \
        .select("fix_advice") \
        .eq("error_code", error_code) \
        .eq("brand", "Bafang") \
        .execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Error code not found in Bafang manual.")
    
    return {
        "bo_says": response.data[0]['fix_advice'],
        "technical_source": "Bafang Dealer Manual"
    }

# Claim Submission (B2B Partner Logic)
@app.post("/claims/submit")
async def submit_claim(claim_data: dict):
    # Logic to flag if it's from a partner shop or retail
    claim_data["claim_source"] = claim_data.get("claim_source", "retail")
    
    response = supabase.table("claims").insert(claim_data).execute()
    return {"status": "Claim logged", "data": response.data}
