"""
Author: Migbert Yanez
GitHub: https://github.com/migbertweb
License: GPL-3.0
Description: Configuración de la base de datos utilizando SQLAlchemy con soporte para múltiples bases de datos (PostgreSQL, SQLite, MariaDB).
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

def get_async_url(url: str) -> str:
    """
    Asegura que la URL de la base de datos utilice el driver asíncrono correcto.
    """
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url

engine = create_async_engine(get_async_url(settings.DATABASE_URL), echo=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    """
    Generador de dependencias para obtener una sesión de base de datos asíncrona.
    """
    async with SessionLocal() as session:
        yield session

