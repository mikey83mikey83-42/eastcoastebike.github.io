import os
from fastapi import FastAPI
from supabase import create_client, Client

# Initialize the FastAPI app
app = FastAPI()

# Supabase configuration
# Replace the placeholders with your actual project URL and Key
url = "YOUR_SUPABASE_URL_HERE"
key = "YOUR_PUBLISHABLE_KEY_HERE"

# Create the Supabase client
supabase: Client = create_client(url, key)

@app.get("/")
async def root():
    return {"message": "Success! Your API is running and connected to Supabase."}

@app.get("/test-db")
async def test_db():
    # A quick check to see if we can talk to your database
    try:
        response = supabase.table("your_table_name").select("*").limit(1).execute()
        return {"status": "Connected", "data": response.data}
    except Exception as e:
        return {"status": "Error", "details": str(e)}
        
