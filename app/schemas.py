"""
Author: Migbert Yanez
GitHub: https://github.com/migbertweb
License: GPL-3.0
Description: Modelos Pydantic (esquemas) para validación de solicitudes y serialización de respuestas, incluyendo definiciones de Token, Usuario y Tarea.
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    """
    Esquema base para Tareas.
    Propiedades comunes para creación, actualización y lectura.
    """
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    """
    Esquema para crear una nueva tarea.
    Hereda de TaskBase, sin campos adicionales requeridos por ahora.
    """
    pass

class TaskUpdate(TaskBase):
    """
    Esquema para actualizar una tarea existente.
    Todos los campos son opcionales.
    """
    title: Optional[str] = None
    completed: Optional[bool] = None

class Task(TaskBase):
    """
    Esquema completo de Tarea para respuestas (leídas desde DB).
    Incluye ID, fecha de creación y ID del propietario.
    """
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    """
    Esquema base para Usuarios.
    """
    email: EmailStr

class UserCreate(UserBase):
    """
    Esquema para crear un nuevo usuario.
    Requiere una contraseña.
    """
    password: str

class User(UserBase):
    """
    Esquema completo de Usuario para respuestas.
    Incluye ID, estado activo y lista de tareas.
    """
    id: int
    is_active: bool
    tasks: list[Task] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    """
    Esquema para el Token de respuesta (JWT).
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Esquema para los datos contenidos en el Token.
    """
    email: Optional[str] = None
