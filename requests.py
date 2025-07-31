from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.mypy.util import serialize_type

from models import async_session, User, Task
from pydantic import BaseModel, ConfigDict
from typing import List

class TaskSchema(BaseModel):
    id: int
    title: str
    completed: bool
    user: int

    model_config = ConfigDict(from_attributes=True)

async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user

        new_user = User(tg_id == tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

async def get_tasks(user_id):
    async with async_session() as session:
        tasks = await session.scalsrs(
            select(Task).where(Task.user == user_id, Task.completed == False)
        )

        serialize_tasks = [
            TaskSchema.model_validate(t).model_dump() for t in tasks
        ]

        return serialize_tasks

async def get_complited_tasks_count(user_id):
    async with async_session() as session:
        return await session.scalar(select(func.count(Task.id)).where(Task.complited == True))