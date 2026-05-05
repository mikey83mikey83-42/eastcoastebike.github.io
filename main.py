from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from supabase import create_client, Client
import os

app = FastAPI()

# --- SUPABASE CONFIGURATION ---
# Paste your specific URL and Key inside the quotes below
SUPABASE_URL = I https://mcp.supabase.com/mcp?project_ref=yytzuwexpaxdfuklxbty
SUPABASE_KEY = "sb_publishable_v8YFBkLK0KXdNvZQKDPDgQ_fqWA4KxU"

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- STATIC FILES & FRONTEND ---
# This mounts the 'src' folder so your CSS/JS files can be found by the HTML
if os.path.exists("src"):
    app.mount("/src", StaticFiles(directory="src"), name="src")

@app.get("/")
async def read_index():
    # This serves your main index.html file to the browser
    return FileResponse('src/index.html')

@app.get("/status")
async def get_status():
    return {
        
