from fastapi import FastAPI

from app.database import Base, engine
import app.models  # noqa: F401 — регистрирует все модели в Base.metadata

app = FastAPI(title="ARTUBE API")


@app.on_event("startup")
def init_db() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"status": "ok", "project": "artube"}