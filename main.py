from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# This is the "secret sauce" that allows your website to talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Claim(BaseModel):
    customer_name: str
    email: str
    serial_number: str
    issue_description: str

@app.get("/inventory")
async def get_inventory():
    return [
        {"id": "B-001", "category": "bike", "name": "Bafang Mid-Drive Cruiser", "price": 1200.00},
        {"id": "P-001", "category": "part", "name": "BBS02 750W Controller", "price": 85.00}
    ]

@app.post("/submit-claim")
async def submit_claim(claim: Claim):
    print(f"New Claim: {claim.serial_number}")
    return {"status": "success"}
  
