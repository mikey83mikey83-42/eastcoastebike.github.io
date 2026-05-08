import os
from uuid import uuid4

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from supabase import create_client, Client
from square.client import Client as SquareClient

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- CONFIGURATION ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SQUARE_ACCESS_TOKEN = os.environ.get("SQUARE_ACCESS_TOKEN")
SQUARE_LOCATION_ID = os.environ.get("SQUARE_LOCATION_ID")
SQUARE_ENVIRONMENT = os.environ.get("SQUARE_ENVIRONMENT", "sandbox")  # sandbox or production

# --- VALIDATION ---
if not SQUARE_ACCESS_TOKEN:
    raise RuntimeError("Missing SQUARE_ACCESS_TOKEN")
if not SQUARE_LOCATION_ID:
    raise RuntimeError("Missing SQUARE_LOCATION_ID")

# --- CLIENTS ---
supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

square_client = SquareClient(
    access_token=SQUARE_ACCESS_TOKEN,
    environment=SQUARE_ENVIRONMENT
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "status": "Ready for Warranty Claims"}
    )

@app.get("/payment-success", response_class=HTMLResponse)
async def payment_success(request: Request):
    return templates.TemplateResponse(
        "success.html",
        {"request": request, "message": "Payment completed successfully."}
    )

@app.post("/submit-claim")
async def handle_claim(
    request: Request,
    customer_name: str = Form(...),
    serial_number: str = Form(...),
    issue: str = Form(...)
):
    claim_data = {
        "customer_name": customer_name,
        "serial_number": serial_number,
        "issue": issue,
        "status": "pending"
    }

    # 1. Save claim to Supabase
    if supabase:
        try:
            supabase.table("claims").insert(claim_data).execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Supabase error: {str(e)}")

    # 2. Create Square checkout link
    try:
        body = {
            "idempotency_key": str(uuid4()),
            "checkout_options": {
                "redirect_url": str(request.base_url).rstrip("/") + "/payment-success"
            },
            "order": {
                "location_id": SQUARE_LOCATION_ID,
                "line_items": [
                    {
                        "name": "Bafang Diagnostic/Warranty Fee",
                        "quantity": "1",
                        "base_price_money": {
                            "amount": 5000,
                            "currency": "USD"
                        }
                    }
                ]
            }
        }

        result = square_client.checkout.create_payment_link(body=body)

        if result.is_success():
            checkout_url = result.body["payment_link"]["url"]
            return RedirectResponse(url=checkout_url, status_code=303)

        raise HTTPException(status_code=400, detail=result.errors)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Square error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
