from fastapi import FastAPI

from app.db.init_db import init_db
from app.api.tasks import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Task Manager API",
    description="API para gestionar tareas personales",
    version="1.0.0"
)

# <<< AÑADIR ESTO >>>
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # dominios permitidos (tu frontend React)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# <<< HASTA AQUÍ >>>

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a Task Manager API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def read_health():
    return {"status": "ok"}


# Registrar las rutas de tareas
app.include_router(tasks_router)
