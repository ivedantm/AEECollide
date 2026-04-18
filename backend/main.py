"""
Dispatch IQ — FastAPI Backend
Wholesale power economics forecasting for BTM gas vs. grid power arbitrage.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.sites import router as sites_router
from backend.routes.dispatch import router as dispatch_router
from backend.routes.replay import router as replay_router

app = FastAPI(
    title="Dispatch IQ API",
    description="BTM gas vs. grid power arbitrage intelligence for ERCOT & WECC",
    version="1.0.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(sites_router)
app.include_router(dispatch_router)
app.include_router(replay_router)


@app.get("/")
def root():
    return {
        "name": "Dispatch IQ API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "sites": "/api/sites",
            "dispatch": "/api/dispatch/current",
            "forecast": "/api/dispatch/forecast",
            "schedule": "/api/dispatch/schedule",
            "briefing": "/api/dispatch/briefing",
            "replay": "/api/replay/uri",
            "docs": "/docs",
        },
    }
