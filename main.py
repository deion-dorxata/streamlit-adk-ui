import os

import uvicorn
from fastapi import FastAPI, Request, APIRouter
from google.adk.cli.fast_api import get_fast_api_app

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Example allowed origins for CORS

# Call the function to get the FastAPI app instance
print("Initializing FastAPI app...")
app: FastAPI = get_fast_api_app(
    agent_dir=AGENT_DIR,
    allow_origins=["*"],
    web=False
)
print("FastAPI app initialized.")

# You can add more FastAPI routes or configurations below if needed
@app.get("/hello")
async def read_root():
    return {"Hello": "World"}

@app.post("/composio/webhook")
async def listen_webhooks(request: Request):
    body = await request.json()
    print("Request Body:", body)
    return {"status": "received"}

# Debug: Print all routes
print("\n=== All Registered Routes ===")
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"{route.path}: {getattr(route, 'methods', 'N/A')}")

if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
