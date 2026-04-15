from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import backend.models as models
import backend.schemas as schemas
from backend.database import SessionLocal

router = APIRouter(prefix="/ejercicio", tags=["Ejercicios"])

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.EjercicioResponse])
def listar_ejercicios(db: Session = Depends(get_db)):
    return db.query(models.Ejercicio).all()
