from fastapi import FastAPI, HTTPException
import uvicorn
from config import is_dev, first_setup
# import database # We will use this later
from setup import router as setup_router

app = FastAPI(
    description="API Backend for Wyra Mood Coder",
    title="Mood Coder API Backend",
    version="alpha"
)

# Include all routers
app.include_router(setup_router)


@app.get("/", summary="Health Check")
async def root():
    return {"status": "healthy", "first_setup": first_setup, "version": app.version}


if __name__ == "__main__":
    print("Starting Mood Coder API Backend...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=is_dev(),
        factory=False,
    )
    print("Stopping Mood Coder API Backend...")