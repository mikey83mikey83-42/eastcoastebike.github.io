import os
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# SILENCE FAVICON 404 (Verified Working)
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content="", media_type="image/x-icon")

# OFFICIAL BUSINESS CONFIG
COMPANY = "East Coast E-bike & Bafang Warranty Claims Rep"
SUPABASE_URL = "https://yytzumexpaxdfuklxbty.supabase.co"
# Note: Ensure this is your Supabase Anon Key
SUPABASE_KEY = "sb_publishable_ghp_5x1JKGeO3OLWd..." 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # This syntax is the most stable for Python 3.12 + FastAPI
    return templates.TemplateResponse(
        "index.html", 
        {"request": request}
    )

@app.post("/submit-claim")
async def handle_claim(
    motor: str = Form(...),
    policy: str = Form(...),
    detail: str = Form(...)
):
    payload = {
        "entity": COMPANY,
        "motor_system": motor,
        "policy_id": policy,
        "issue_description": detail,
        "status": "Awaiting BESST Pro Diagnostics"
    }

    try:
        # Wrapping in a list [payload] fixes the database-side TypeError
        supabase.table("claims").insert([payload]).execute()
        return {"status": "Success", "message": "Claim submitted successfully"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "Error", "message": str(e)}
        
