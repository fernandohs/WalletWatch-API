from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.db.session import engine
from app.models import transaction
from app.routers import transactions
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    title="WalletWatch API",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(transactions.router, prefix=settings.API_V1_STR + "/transactions", tags=["Transactions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to WalletWatch API 🚀"}