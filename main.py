import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Setup for templates and static files
# Make sure these folders exist in your root directory
templates = Jinja2Templates(directory="templates")

# Favicon route to prevent 404 errors in logs
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('static/favicon.ico')

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Renders the main landing page for the East Coast E-bike 
    & Bafang Warranty Claims Repair Center.
    """
    # FIXED: Template name "index.html" MUST come first.
    # The dictionary with "request" is the second argument.
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Bafang Warranty Hub"}
    )

@app.post("/submit-claim")
async def handle_claim(
    request: Request,
    customer_name: str = Form(...),
    serial_number: str = Form(...),
    issue_description: str = Form(...)
):
    """
    Endpoint for handling Bafang warranty claim submissions.
    This is where your Supabase integration logic will live.
    """
    # Logic for Supabase / Database insertion goes here
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "message": f"Claim received for {customer_name}. We will review the motor/battery logs."
        }
    )

if __name__ == "__main__":
    import uvicorn
    # Standard port for Render/Termux testing
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
