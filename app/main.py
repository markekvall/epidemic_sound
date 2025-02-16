from fastapi import FastAPI
from app.api.sound_controller import router
from app.infrastructure.database import init_db

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()
