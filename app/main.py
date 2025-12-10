from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from contextlib import asynccontextmanager

from . import crud, models, schemas
from .database import engine, get_db, Base

# Crear las tablas al iniciar (solo para desarrollo/ejemplo simple sin migraciones como alembic)
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Gestor de Tareas API", description="API para gestionar tareas con FastAPI y Postgres", lifespan=lifespan)

@app.post("/tasks/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Crear una nueva tarea.
    - **title**: Título de la tarea (obligatorio)
    - **description**: Descripción opcional
    - **completed**: Estado de la tarea (por defecto False)
    """
    return await crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=List[schemas.Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Obtener lista de tareas con paginación.
    """
    tasks = await crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtener una tarea específica por ID.
    """
    db_task = await crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    """
    Actualizar una tarea.
    Solo envía los campos que deseas actualizar.
    """
    db_task = await crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Eliminar una tarea.
    """
    db_task = await crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"ok": True}
