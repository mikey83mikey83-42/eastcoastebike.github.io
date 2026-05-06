import os
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from supabase import create_client, Client
from square.client import Client as SquareClient

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- CONFIGURATION (Render/Termux Environment Variables) ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SQUARE_ACCESS_TOKEN = os.environ.get("SQUARE_ACCESS_TOKEN")
SQUARE_LOCATION_ID = os.environ.get("SQUARE_LOCATION_ID")

# Initialize Clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None

# Square for payment processing
square_client = SquareClient(
    access_token=SQUARE_ACCESS_TOKEN,
    environment='production' # Set to 'sandbox' in Render env vars for testing
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Landing page for East Coast E-bike Warranty Hub."""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "status": "Ready for Warranty Claims"}
    )

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
        if supabase:
            supabase.table("claims").insert(data).execute()
    except Exception as e:
        print(f"Supabase Error: {e}")

    # 2. CREATE SQUARE CHECKOUT LINK ($50 Diagnostic Fee)
    try:
        body = {
            "idempotency_key": os.urandom(12).hex(),
            "checkout_options": {
                "redirect_url": str(request.base_url)
            },
            "order": {
                "location_id": SQUARE_LOCATION_ID,
                "line_items": [{
                    "name": "Bafang Diagnostic/Warranty Fee",
                    "quantity": "1",
                    "base_price_money": {
                        "amount": 5000, # $50.00
                        "currency": "USD"
                    }
                }]
            }
        }

        result = square_client.checkout.create_payment_link(body=body)

        if result.is_success():
            checkout_url = result.body['payment_link']['url']
            return RedirectResponse(url=checkout_url, status_code=303)
        else:
            raise HTTPException(status_code=400, detail=str(result.errors))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # This line is key: it looks for PORT first, then defaults to 10000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
