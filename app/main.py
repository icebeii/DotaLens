from fastapi import FastAPI

from app.api.players import router as players_router

app = FastAPI(
    title="DotaLens API",
    description="Backend for Dota 2 analytics",
    version="0.1.0",
)

app.include_router(players_router)

@app.get("/")
async def root():
    return {
        "name": "DotaLens",
        "version": "0.1.0",
        "status": "ok",
    }
