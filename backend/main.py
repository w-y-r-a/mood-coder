from fastapi import FastAPI, HTTPException
import uvicorn
from config import is_dev, first_setup, OLLAMA_HOST
from database import close_db_connection, init_db
from contextlib import asynccontextmanager
from setup import router as setup_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield  # Application is running
    await close_db_connection()  # This runs on shutdown


app = FastAPI(
    description="API Backend for Wyra Mood Coder",
    title="Mood Coder API Backend",
    version="alpha",
    lifespan=lifespan,
)

# Include all routers
app.include_router(setup_router)
if not first_setup:
    if OLLAMA_HOST:
        from ai._ollama import router as ollama_router
        app.include_router(ollama_router)


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