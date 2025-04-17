from fastapi import FastAPI
from app.routes import router as campaign_router

def create_app() -> FastAPI:
    app = FastAPI(title="Discount Campaign Management")
    app.include_router(campaign_router, prefix="/api")
    return app
