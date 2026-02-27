from fastapi import FastAPI

from backend.api.auth import router as auth_router

app = FastAPI(title="Backend API")

app.include_router(auth_router)
