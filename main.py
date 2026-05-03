from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# This is what people will see when they visit your URL
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>East Coast Ebike Warranty</title>
        <style>
            body { 
                font-family: sans-serif; 
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                justify-content: center; 
                height: 100vh; 
                margin: 0;
                background-color: #f4f4f4;
            }
            .container {
                text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>East Coast Ebike Warranty</h1>
            <p>Your site is officially live and serving HTML!</p>
        </div>
    </body>
    </html>
    """

# Keeps the deployment healthy
@app.get("/health")
async def health_check():
    return {"status": "ok"}
