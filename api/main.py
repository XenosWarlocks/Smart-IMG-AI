# api/main.py
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict
from pathlib import Path
import sys
import uvicorn

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Local imports
from backend.image_captioning import ImageCaptioningSystem
from backend.img_pro import ImageProcessor
from .token_tracker import TokenTracker

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
STATIC_DIR = Path(__file__).resolve().parent / 'static'
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Global token tracker
token_tracker = TokenTracker()

# Updated request models to match the actual request structure
class ImageURL(BaseModel):
    url: str

class APIKeyConfig(BaseModel):
    key1: str
    key2: str

@app.get("/")
async def read_root():
    return FileResponse(str(STATIC_DIR / 'index.html'))

@app.get("/api/usage")
async def get_usage():
    return token_tracker.get_usage_stats()

@app.post("/api/analyze-image-url")
async def analyze_image_url(image_data: ImageURL, api_keys: APIKeyConfig):
    try:
        if not image_data.url:
            raise HTTPException(
                status_code=400,
                detail="Missing required field: url"
            )

        # Initialize captioning system
        system = ImageCaptioningSystem(api_keys.key1, api_keys.key2)
        
        # Process image and get components and token usage
        components, usage = system.process_image(image_data.url)
        
        # Update token tracker
        token_tracker.update_usage(1, usage['key1'])
        token_tracker.update_usage(2, usage['key2'])
        
        return {
            "success": True,
            "components": components,
            "token_usage": token_tracker.get_usage_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-image-upload")
async def analyze_image_upload(
    file: UploadFile = File(...),
    api_key1: str = Form(...),
    api_key2: str = Form(...)
):
    try:
        if not file:
            raise HTTPException(
                status_code=400,
                detail="Missing required field: file"
            )

        # Initialize captioning system
        system = ImageCaptioningSystem(api_key1, api_key2)
        
        # Read file contents
        contents = await file.read()
        
        # Process image and get components and token usage
        components, usage = system.process_image(contents)
        
        # Update token tracker
        token_tracker.update_usage(1, usage['key1'])
        token_tracker.update_usage(2, usage['key2'])
        
        return {
            "success": True,
            "components": components,
            "token_usage": token_tracker.get_usage_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# python -m uvicorn api.main:app --reload