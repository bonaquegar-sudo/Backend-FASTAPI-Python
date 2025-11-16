from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)) -> TaskRead:
    task = Task(
        title=task_in.title,
        description=task_in.description,
        completed=task_in.completed,
        priority=task_in.priority,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=List[TaskRead])
def list_tasks(
    completed: Optional[bool] = None,
    min_priority: int = Query(1, ge=1, le=5),
    max_priority: int = Query(5, ge=1, le=5),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[TaskRead]:
    """
    Listar tareas con filtros y paginación:
    - completed: True/False para filtrar por estado
    - min_priority, max_priority: rango de prioridad (1-5)
    - skip: cuántos registros saltar (paginación)
    - limit: cuántos registros devolver como máximo
    """
    query = db.query(Task)

    # Filtro por estado (solo si el cliente lo envía)
    if completed is not None:
        query = query.filter(Task.completed == completed)

    # Filtro por rango de prioridad
    query = query.filter(Task.priority >= min_priority, Task.priority <= max_priority)

    # Orden por fecha de creación (más recientes primero)
    query = query.order_by(Task.created_at.desc())

    # Paginación
    tasks = query.offset(skip).limit(limit).all()
    return tasks



@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskRead:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db)
) -> TaskRead:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    update_data = task_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    db.delete(task)
    db.commit()
    return None
