from fastapi import FastAPI, Request
from supabase import create_client, Client
import os

app = FastAPI()

# Use sandbox environment variables
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.get("/")
async def root():
    return {"message": "East Coast E-bike Warranty Claims API"}

@app.post("/submit-claim")
async def submit_claim(data: dict):
    # Logic for Bafang 2027 system models
    response = supabase.table("claims").insert(data).execute()
    return response
