from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# This links your 'src' folder so CSS/JS files can be found
# Make sure your folder is actually named 'src' in GitHub
app.mount("/src", StaticFiles(directory="src"), name="src")

@app.get("/")
async def read_index():
    # This sends the index.html file to the browser
    return FileResponse(os.path.join("src", "index.html"))
    
