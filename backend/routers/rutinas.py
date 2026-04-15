from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import backend.models as models
import backend.schemas as schemas
from backend.database import SessionLocal

router = APIRouter(tags=["Rutinas"])

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- ENDPOINTS DE TIPOS DE RUTINA ---

@router.get("/tipo-rutina", response_model=List[schemas.TipoRutinaResponse])
def listar_tipos_rutina(db: Session = Depends(get_db)):
    """Trae los tipos (Fuerza, Hipertrofia, etc.)"""
    return db.query(models.TipoRutina).all()

# --- ENDPOINTS DE RUTINAS ---

@router.post("/rutina", response_model=schemas.RutinaResponse)
def crear_rutina(rutina_in: schemas.RutinaCreate, db: Session = Depends(get_db)):
    # 1. Creamos la cabecera de la rutina vinculada al alumno
    nueva_rutina = models.Rutina(
        nombre=rutina_in.nombre,
        alumno_id=rutina_in.alumno_id, # <--- ASIGNACIÓN CLAVE
        tipo_rutina_id=rutina_in.tipo_rutina_id,
        fecha_desde=rutina_in.fecha_desde,
        fecha_hasta=rutina_in.fecha_hasta,
        vigente=rutina_in.vigente
    )
    
    db.add(nueva_rutina)
    db.commit()
    db.refresh(nueva_rutina)

    # 2. Guardamos los ejercicios (esto ya lo teníamos, pero ahora están unidos al ID de arriba)
    for ej in rutina_in.ejercicios:
        detalle = models.EjercicioDetalle(
            rutina_id=nueva_rutina.id,
            ejercicio_id=ej.ejercicio_id,
            series=ej.series,
            repeticiones=ej.repeticiones,
            orden=ej.orden
        )
        db.add(detalle)
    
    db.commit()
    db.refresh(nueva_rutina)
    return nueva_rutina

@router.get("/rutina", response_model=List[schemas.RutinaResponse])
def listar_todas_las_rutinas(db: Session = Depends(get_db)):
    return db.query(models.Rutina).all()