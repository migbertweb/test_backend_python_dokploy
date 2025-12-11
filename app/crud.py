"""
Author: Migbert Yanez
GitHub: https://github.com/migbertweb
License: GPL-3.0
Description: Functions for Create, Read, Update, and Delete (CRUD) operations on the database for Users and Tasks.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from .auth import get_password_hash

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id))
    return result.scalars().first()

async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Task).offset(skip).limit(limit))
    return result.scalars().all()

async def create_task(db: AsyncSession, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.model_dump(), owner_id=user_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task(db: AsyncSession, task_id: int, task: schemas.TaskUpdate):
    db_task = await get_task(db, task_id)
    if db_task:
        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
    return db_task

async def delete_task(db: AsyncSession, task_id: int):
    db_task = await get_task(db, task_id)
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task
