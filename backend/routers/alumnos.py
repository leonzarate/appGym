from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import backend.models as models
import backend.schemas as schemas
from backend.database import SessionLocal

router = APIRouter(prefix="/alumno", tags=["Alumnos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.AlumnoResponse])
def listar_alumnos(db: Session = Depends(get_db)):
    return db.query(models.Alumno).all()

@router.get("/listado", response_model=List[schemas.AlumnoResponse2])
def listar_nombres_alumnos(db: Session = Depends(get_db)):
    return db.query(models.Alumno).all()

@router.get("/{alumno_id}", response_model=schemas.AlumnoResponse)
def detalle_alumno(alumno_id: int, db: Session = Depends(get_db)):
    db_alumno = db.query(models.Alumno).filter(models.Alumno.id == alumno_id).first()
    if not db_alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return db_alumno