import os
import base64
import json
import requests
from fastapi import FastAPI

app = FastAPI()

# --- CONFIGURATION (Set these in Render Env Vars) ---
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")
REPO_NAME = "mikey83mikey83-42/eastcoastebike.github.io" 
DB_FILE = "repairs.json"

# --- HELPERS ---
def save_to_github(new_data):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{DB_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    # Get the file to find the 'sha' and current content
    r = requests.get(url, headers=headers).json()
    sha = r['sha']
    content = json.loads(base64.b64decode(r['content']))
    
    content.append(new_data)
    
    # Push update
    updated_b64 = base64.b64encode(json.dumps(content, indent=4).encode()).decode()
    payload = {"message": "Automated log update", "content": updated_b64, "sha": sha}
    requests.put(url, headers=headers, json=payload)

# --- ROUTES ---
@app.get("/")
async def root():
    return {"status": "Online", "service": "East Coast E-Bike API", "database": "GitHub-Linked"}

@app.post("/log-repair")
async def log_repair(customer: str, motor: str, tracking: str):
    # 1. Prepare data entry
    entry = {
        "customer": customer,
        "motor": motor,
        "tracking": tracking,
        "status": "Shipped",
        "timestamp": "2026-04-23"
    }
    
    # 2. Save to GitHub automatically
    save_to_github(entry)
    
    return {"message": f"Ol' boy, {customer}'s repair is logged and live!"}
    
