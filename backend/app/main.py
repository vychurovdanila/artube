from fastapi import FastAPI

app = FastAPI(title="ARTUBE API")

@app.get("/")
def read_root():
    return {"status": "ok", "project": "artube"}