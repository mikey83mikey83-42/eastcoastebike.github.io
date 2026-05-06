import os
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from supabase import create_client, Client
import stripe

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- CONFIGURATION (Uses Render/Termux Env Vars) ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

# Initialize Clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None
stripe.api_key = STRIPE_SECRET_KEY

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit-claim")
async def handle_claim(
    request: Request,
    customer_name: str = Form(...),
    serial_number: str = Form(...),
    issue: str = Form(...)
):
    # 1. SAVE TO SUPABASE
    try:
        data = {
            "customer_name": customer_name,
            "serial_number": serial_number,
            "issue": issue,
            "status": "pending"
        }
        # Assuming your table is named 'claims'
        supabase.table("claims").insert(data).execute()
    except Exception as e:
        print(f"Supabase Error: {e}")
        # We keep going so the user isn't blocked, but log it

    # 2. CREATE STRIPE CHECKOUT (e.g., for a $50 diagnostic fee)
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Bafang Diagnostic Fee'},
                    'unit_amount': 5000, # $50.00
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=str(request.base_url),
            cancel_url=str(request.base_url),
        )
        return HTMLResponse(f'<html><body><script>window.location.href="{checkout_session.url}"</script></body></html>')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
