from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..dependencies import get_db

router = APIRouter()

projectNotFoundException = HTTPException(status_code=404, detail="Project not found")

@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_project = models.Project(**project.model_dump(), owner_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    projects = db.query(models.Project).filter(models.Project.owner_id == current_user.id).offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == current_user.id).first()
    if project is None:
        raise projectNotFoundException
    return project

@router.put("/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == current_user.id).first()
    if db_project is None:
        raise projectNotFoundException
    for key, value in project.model_dump().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == current_user.id).first()
    if db_project is None:
        raise projectNotFoundException
    db.delete(db_project)
    db.commit()
    return db_project
