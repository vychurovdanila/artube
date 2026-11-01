from fastapi import FastAPI

from app.api import auth as auth_router
from app.database import Base, engine
import app.models  # noqa: F401

app = FastAPI(title="ARTUBE API")

app.include_router(auth_router.router)


@app.on_event("startup")
def init_db() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"status": "ok", "project": "artube"}