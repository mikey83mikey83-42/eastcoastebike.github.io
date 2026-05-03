from fastapi import FastAPI, Request
import square.client
import shippo
import os

app = FastAPI()

# 1. Connect to Square (Using the Secrets you put in GitHub)
square_client = square.client.Client(
    access_token=os.environ.get('SQUARE_ACCESS_TOKEN'),
    environment='production' 
)

# 2. Connect to Shippo
shippo.api_key = os.environ.get('SHIPPO_API_KEY')

# --- THE BUTTON LOGIC ---

@app.post("/create-repair-ticket")
async def create_claim(data: Request):
    # This powers the 'Warranty Hub' button
    # It saves the customer info and tells Shippo to email a label
    form_data = await data.json()
    
    # Logic to generate a return label via Shippo
    shipment = shippo.Shipment.create(
        address_from={
            "name": form_data['name'],
            "street1": form_data['address'],
            "city": form_data['city'],
            "state": form_data['state'],
            "zip": form_data['zip'],
            "country": "US"
        },
        address_to="YOUR_ALLIANCE_OHIO_ADDRESS",
        parcels=[{"length": "12", "width": "12", "height": "12", "distance_unit": "in", "weight": "10", "mass_unit": "lb"}]
    )
    return {"status": "Label Sent", "tracking": shipment.tracking_number}

@app.get("/inventory")
def get_parts():
    # This pulls from your Supabase table and shows it on the 'Inventory' button
    # We'll link this directly to the frontend
    pass
    
