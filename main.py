import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- OFFICIAL AFFILIATE CONFIG ---
COMPANY_NAME = "East Coast E-bike Warranty Claims Repair Center LLC"
SUPABASE_URL = "https://yytzuwexpaxdfuklxbty.supabase.co"
SUPABASE_KEY = "sb_publishable_v8YFBkLK0KXdNvZQKDPDgQ_fqWA4KxU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "company": COMPANY_NAME
    })

@app.post("/submit-claim")
async def handle_claim(
    motor_model: str = Form(...), 
    policy_num: str = Form(...), 
    issue: str = Form(...)
):
    # Logs claim with official Bafang 2027 motor models
    data = {
        "company": COMPANY_NAME,
        "motor_model": motor_model,
        "policy_number": policy_num,
        "description": issue,
        "status": "Pending Legal Review"
    }
    try:
        supabase.table("claims").insert(data).execute()
        return {"status": "Success", "message": f"Claim received by {COMPANY_NAME}."}
    except Exception as e:
        return {"error": str(e)}
        
