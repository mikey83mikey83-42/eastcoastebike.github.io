import os
from fastapi import FastAPI
from square.client import Client

app = FastAPI(title="East Coast Regional Hub: Motors & Repairs")

# Square Setup
access_token = os.environ.get('SQUARE_ACCESS_TOKEN')
client = Client(access_token=access_token, environment='sandbox')

@app.get("/")
def hub_status():
    return {
        "hub": "East Coast Regional Warranty Center",
        "specialties": ["Mid-drive Systems", "Hub Motors", "Board-level Micro-soldering"],
        "status": "Ready for Intake"
    }

# --- DEALER INVENTORY (Selling Products) ---
@app.get("/inventory/motors")
def get_motor_stock():
    """
    Pulls live dealer stock for Mid-drives and Hub motors from Square.
    """
    result = client.catalog.list_catalog(types='ITEM')
    if result.is_success():
        items = result.body.get('objects', [])
        # Filter for specific motor types in your Square Catalog
        inventory = {
            "mid_drive": [i for i in items if "mid" in i['item_data']['name'].lower()],
            "hub_motor": [i for i in items if "hub" in i['item_data']['name'].lower()],
            "electronics": [i for i in items if "controller" in i['item_data']['name'].lower()]
        }
        return inventory
    return {"error": "Could not sync with Square Inventory"}

# --- TECHNICAL SERVICE (Board Level Repairs) ---
@app.post("/service/intake")
def repair_intake(motor_type: str, serial: str, fault: str):
    """
    Endpoint for logging Mid-drive or Hub motor repairs.
    Example motor_type: 'Mid-drive' or 'Battery BMS'
    """
    return {
        "status": "Intake Success",
        "technician": "Regional Hub East",
        "unit": motor_type,
        "serial_logged": serial,
        "diagnosis_queue": "High Priority"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
    
