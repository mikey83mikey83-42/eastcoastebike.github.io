if __name__ == "__main__":
    import uvicorn
    import os
    # Render provides the PORT environment variable automatically
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
