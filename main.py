import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- OFFICIAL BUSINESS CONFIG ---
COMPANY = "East Coast E-bike Warranty Claims Repair Center LLC"
SUPABASE_URL = "https://yytzuwexpaxdfuklxbty.supabase.co"
SUPABASE_KEY = "sb_publishable_v8YFBkLK0KXdNvZQKDPDgQ_fqWA4KxU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "company": COMPANY})

@app.post("/submit-claim")
async def handle_claim(
    "motor": str = Form(...), 
    "policy": str = Form(...), 
    "detail": str = Form(...)
):
    # Logs claim for East Coast E-bike & Bafang Affiliate systems
    payload = {
        "entity": COMPANY,
        "motor_system": motor,
        "policy_id": policy,
        "issue_description": detail,
        "status": "Awaiting BESST Pro Diagnostics"
    }
    try:
        supabase.table("claims").insert(payload).execute()
        return {"status": "Success", "message": f"Claim filed with {COMPANY}. Our team will contact you shortly."}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
        
