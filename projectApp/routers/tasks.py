from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..dependencies import get_db

router = APIRouter()

taskNotFoundException = HTTPException(status_code=404, detail="Task not found")

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == current_user.id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db_task = models.Task(**task.model_dump(), project_id=project_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[schemas.Task])
def read_tasks(project_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    tasks = db.query(models.Task).join(models.Project).filter(models.Task.project_id == project_id, models.Project.owner_id == current_user.id).offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).join(models.Project).filter(models.Task.id == task_id, models.Project.owner_id == current_user.id).first()
    if task is None:
        raise taskNotFoundException
    return task

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_task = db.query(models.Task).join(models.Project).filter(models.Task.id == task_id, models.Project.owner_id == current_user.id).first()
    if db_task is None:
        raise taskNotFoundException
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_task = db.query(models.Task).join(models.Project).filter(models.Task.id == task_id, models.Project.owner_id == current_user.id).first()
    if db_task is None:
        raise taskNotFoundException
    db.delete(db_task)
    db.commit()
    return db_task
