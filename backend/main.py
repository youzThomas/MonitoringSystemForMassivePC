from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from veyon_client import VeyonClient
import uvicorn

# Initialize FastAPI app and Veyon client
app = FastAPI()
veyon = VeyonClient()

# Authentication endpoint
@app.post("/auth")
async def authenticate(auth_method: str, credentials: dict):
    try:
        return veyon.authenticate(auth_method, credentials)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Screenshot endpoint
@app.get("/screenshot")
async def get_screenshot():
    try:
        return Response(content=veyon.get_screenshot(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Screen lock endpoint
@app.post("/lock-screens")
async def lock_screens():
    try:
        success = veyon.lock_screens()
        return {"status": "success" if success else "failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Main entry point to run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)