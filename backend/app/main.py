from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.models import *  # noqa: F401,F403
from app.routers import assistant, auth, collections, dashboard, dropoffs, feedback, rewards

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Setu API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(dropoffs.router, prefix="/dropoffs", tags=["dropoffs"])
app.include_router(collections.router, prefix="/collections", tags=["collections"])
app.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(assistant.router, prefix="/assistant", tags=["assistant"])


@app.get("/")
def root():
    return {"status": "E-Setu API running"}
