"""
Author: Migbert Yanez
GitHub: https://github.com/migbertweb
License: GPL-3.0
Description: Punto de entrada principal para la aplicación FastAPI. Configura la aplicación, el middleware, la conexión a la base de datos y define las rutas de la API para usuarios y tareas.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from contextlib import asynccontextmanager
from typing import Annotated
from datetime import timedelta
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

from . import crud, models, schemas, auth, deps
from .database import engine, get_db, Base

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para registrar cada solicitud HTTP que entra a la aplicación.
    Mide el tiempo de procesamiento y registra el método, URL y código de estado.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.4f}s")
        return response

# Configuración de límites de velocidad (Rate Limiting)
limiter = Limiter(key_func=get_remote_address)

# Configuración para crear tablas al inicio
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de contexto para el ciclo de vida de la aplicación.
    Crea las tablas de la base de datos al iniciar la aplicación.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Gestor de Tareas API", description="API para gestionar tareas con FastAPI y Postgres", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=schemas.Token)
@limiter.limit("5/minute")
async def login_for_access_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    """
    Endpoint para autenticar usuarios y obtener un token de acceso (JWT).
    """
    user = await crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
@limiter.limit("5/minute")
async def create_user(request: Request, user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return await crud.create_user(db=db, user=user)

@app.post("/tasks/", response_model=schemas.Task)
@limiter.limit("10/minute")
async def create_task(request: Request, task: schemas.TaskCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(deps.get_current_user)):
    """
    Crear una nueva tarea.
    """
    return await crud.create_task(db=db, task=task, user_id=current_user.id)

@app.get("/tasks/", response_model=List[schemas.Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(deps.get_current_user)):
    """
    Obtener lista de tareas con paginación.
    """
    # Nota: En una aplicación real, querríamos filtrar solo por el propietario
    # tasks = await crud.get_tasks(db, skip=skip, limit=limit)
    # Por ahora devolvemos todas, similar al estado anterior, pero se requiere autenticación
    tasks = await crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(deps.get_current_user)):
    """
    Obtener una tarea específica por ID.
    """
    db_task = await crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(deps.get_current_user)):
    """
    Actualizar una tarea.
    """
    db_task = await crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(deps.get_current_user)):
    """
    Eliminar una tarea.
    """
    db_task = await crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"ok": True}
