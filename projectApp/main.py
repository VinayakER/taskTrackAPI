from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import users, projects, tasks
from . import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(auth.router, prefix="", tags=["auth"])
