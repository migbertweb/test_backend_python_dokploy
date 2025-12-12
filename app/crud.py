"""
Author: Migbert Yanez
GitHub: https://github.com/migbertweb
License: GPL-3.0
Description: Funciones para operaciones Crear, Leer, Actualizar y Eliminar (CRUD) en la base de datos para Usuarios y Tareas.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models, schemas
from .auth import get_password_hash

async def get_user(db: AsyncSession, user_id: int):
    """
    Obtiene un usuario por su ID.
    """
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    """
    Obtiene un usuario por su correo electrónico.
    """
    result = await db.execute(select(models.User).options(selectinload(models.User.tasks)).filter(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """
    Crea un nuevo usuario en la base de datos con contraseña hasheada.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    # Manually construct the Pydantic model to avoid async lazy loading of 'tasks'
    return schemas.User(
        id=db_user.id,
        email=db_user.email,
        is_active=db_user.is_active,
        tasks=[]
    )

async def get_task(db: AsyncSession, task_id: int):
    """
    Obtiene una tarea por su ID.
    """
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id))
    return result.scalars().first()

async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de tareas con paginación (skip y limit).
    """
    result = await db.execute(select(models.Task).offset(skip).limit(limit))
    return result.scalars().all()

async def create_task(db: AsyncSession, task: schemas.TaskCreate, user_id: int):
    """
    Crea una nueva tarea asignada a un usuario.
    """
    db_task = models.Task(**task.model_dump(), owner_id=user_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task(db: AsyncSession, task_id: int, task: schemas.TaskUpdate):
    """
    Actualiza una tarea existente.
    """
    db_task = await get_task(db, task_id)
    if db_task:
        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
    return db_task

async def delete_task(db: AsyncSession, task_id: int):
    """
    Elimina una tarea por su ID.
    """
    db_task = await get_task(db, task_id)
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task

