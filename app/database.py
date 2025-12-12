"""
Author: Migbert Yanez
GitHub: https://github.com/migbertweb
License: GPL-3.0
Description: Configuración de la base de datos utilizando SQLAlchemy y AsyncPG para conexiones asíncronas.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuración de la aplicación utilizando Pydantic BaseSettings.
    Lee las variables de entorno para la configuración de la base de datos y JWT.
    """
    # PostgreSQL (Por defecto)
    # DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    
    # SQLite (Descomentar para usar)
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    
    # MariaDB / MySQL (Descomentar para usar)
    # DATABASE_URL: str = "mysql+aiomysql://user:password@localhost/dbname"

    SECRET_KEY: str = "YOUR_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    echo_sql: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

engine = create_async_engine(settings.DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    """
    Generador de dependencias para obtener una sesión de base de datos asíncrona.
    """
    async with SessionLocal() as session:
        yield session

