from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth as auth_router
from app.api import artworks as artworks_router
from app.api import users as users_router
from app.database import Base, engine
import app.models  # noqa: F401

app = FastAPI(title="ARTUBE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(artworks_router.router)
app.include_router(users_router.router)


@app.on_event("startup")
def init_db() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"status": "ok", "project": "artube"}