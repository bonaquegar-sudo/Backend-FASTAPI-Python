from app.db.session import Base, engine
from app.models.task import Task  # Importa el modelo para que SQLAlchemy lo "vea"


def init_db():
    """Crea todas las tablas en la BD si no existen"""
    Base.metadata.create_all(bind=engine)
