from fastapi import FastAPI
from .routers.health import router as health_router
from .routers.wallet import router as wallet_router
from .routers.checkout import router as checkout_router

app = FastAPI(title="SkyPay & Rewards Hub", version="0.1.0")
app.include_router(health_router, prefix="")
app.include_router(wallet_router, prefix="/wallet")
app.include_router(checkout_router, prefix="")

# Root info
@app.get("/")
def root():
    return {"name": "SkyPay & Rewards Hub", "version": "0.1.0", "docs": "/docs"}
