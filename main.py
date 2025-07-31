from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
import requests as rq


@asynccontextmanager
async def lifespan(app_:FastAPI):
    await init_db()
    print("Bot is ready")
    yield

app = FastAPI(title="To Do App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_method=["*"],
    allow_headers=["*"]
)

@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_tasks(user.id)

@app.get("/api/main/{tg.id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id)
    complited_tasks_count = await rq.get_complited_tasks_count(user.id)
    return {'complitedTasks': complited_tasks_count}
