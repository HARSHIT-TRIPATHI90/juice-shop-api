from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from .seed import init_db_and_seed
from .routers import auth, products, basket, orders, feedback, addresses, admin

app = FastAPI(
    title="Juice Lab API",
    description=(
        "A from-scratch FastAPI rebuild of the OWASP Juice Shop product/user "
        "data, built as a clean baseline before intentional vulnerabilities "
        "are layered in. Educational use only."
    ),
    version="0.1.0",
)


@app.on_event("startup")
def on_startup():
    init_db_and_seed()


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(basket.router)
app.include_router(orders.router)
app.include_router(feedback.router)
app.include_router(addresses.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
