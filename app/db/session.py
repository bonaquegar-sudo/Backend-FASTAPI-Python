from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a SQLite
# Se creará un archivo "task_manager.db" en la carpeta raíz del proyecto
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"

# Crear el engine (conexión a BD)
# check_same_thread=False: permite que múltiples threads usen la misma conexión (necesario para SQLite en desarrollo)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# SessionLocal: fábrica para crear sesiones de BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase base que heredarán todos los modelos
Base = declarative_base()

from typing import Generator
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
