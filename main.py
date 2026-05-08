import logging
import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field
from square import Square as SquareClient
from supabase import create_client, Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SQUARE_ACCESS_TOKEN = os.environ.get("SQUARE_ACCESS_TOKEN")
SQUARE_LOCATION_ID = os.environ.get("SQUARE_LOCATION_ID")
SQUARE_ENVIRONMENT = os.environ.get("SQUARE_ENVIRONMENT", "sandbox")
WARRANTY_FEE_CENTS = int(os.environ.get("WARRANTY_FEE_CENTS", "5000"))
CURRENCY = os.environ.get("CURRENCY", "USD")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing Supabase configuration")
if not SQUARE_ACCESS_TOKEN:
    raise RuntimeError("Missing SQUARE_ACCESS_TOKEN")
if not SQUARE_LOCATION_ID:
    raise RuntimeError("Missing SQUARE_LOCATION_ID")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mikey83mikey83-42.github.io",
        "https://eastcoastebike.github.io",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

square_client = SquareClient(
    access_token=SQUARE_ACCESS_TOKEN,
    environment=SQUARE_ENVIRONMENT,
)

class ClaimRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    serial_number: str = Field(..., min_length=3, max_length=100)
    issue_description: str = Field(..., min_length=10, max_length=2000)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "status": "Ready for Warranty Claims"},
    )

@app.get("/payment-success", response_class=HTMLResponse)
async def payment_success(request: Request):
    return templates.TemplateResponse(
        "success.html",
        {"request": request, "message": "Payment completed successfully."},
    )

@app.post("/submit-claim")
async def handle_claim(request: Request, payload: ClaimRequest):
    claim_data = {
        "customer_name": payload.customer_name.strip(),
        "email": payload.email.strip(),
        "serial_number": payload.serial_number.strip(),
        "issue": payload.issue_description.strip(),
        "status": "pending",
        "payment_status": "unpaid",
    }

    try:
        supabase.table("claims").insert(claim_data).execute()
        logger.info("Claim saved to Supabase")
    except Exception:
        logger.exception("Supabase insert failed")
        raise HTTPException(status_code=500, detail="Failed to save claim")

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
                            "amount": WARRANTY_FEE_CENTS,
                            "currency": CURRENCY,
                        },
                    }
                ],
            },
        }

        result = square_client.checkout.create_payment_link(body=body)

        if result.is_success():
            checkout_url = result.body["payment_link"]["url"]
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "Claim submitted successfully",
                    "checkout_url": checkout_url,
                },
            )

        logger.error("Square error response: %s", result.errors)
        raise HTTPException(status_code=400, detail="Failed to create payment link")

    except HTTPException:
        raise
    except Exception:
        logger.exception("Square payment link creation failed")
        raise HTTPException(status_code=500, detail="Payment provider error")

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
