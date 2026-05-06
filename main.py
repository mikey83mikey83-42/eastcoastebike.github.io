import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI app
app = FastAPI()

# Configure Templates - Ensure your 'templates' folder exists in the root
templates = Jinja2Templates(directory="templates")

# Mount Static Files (for CSS, JS, and your logo/favicon)
# Create a folder named 'static' if you haven't already
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Favicon route to keep logs clean and prevent 404s
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    if os.path.exists('static/favicon.ico'):
        return FileResponse('static/favicon.ico')
    return HTMLResponse(status_code=204)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Main landing page for East Coast E-bike & Bafang Warranty Hub.
    """
    # FIXED: "index.html" is now the first argument (fixes the TypeError)
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "status": "Ready for Bafang Repairs"}
    )

@app.post("/submit-claim")
async def handle_claim(
    request: Request,
    customer_name: str = Form(...),
    serial_number: str = Form(...),
    issue_details: str = Form(...)
):
    """
    Handle warranty claim submissions. 
    This connects to your automated business logic.
    """
    # This is where your Supabase / Stripe logic will trigger
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "message": f"Success! Claim for {customer_name} has been queued for review."
        }
    )

# Health check endpoint for Render deployment
@app.get("/health")
async def health_check():
    return {"status": "active", "environment": "Render/Termux"}

if __name__ == "__main__":
    import uvicorn
    # Render provides the PORT environment variable automatically
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
