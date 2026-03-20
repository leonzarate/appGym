from fastapi.middleware.cors import CORSMiddleware # IMPORTANTE
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from typing import List
import models, schemas  # Importamos nuestros esquemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS: Permite que tu frontend hable con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción pondrás tu URL de Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RUTAS ---
# 1. CREATE: Crear un alumno
@app.post("/alumno", response_model=schemas.AlumnoResponse)
def crear_alumno(alumno: schemas.AlumnoCreate, db: Session = Depends(get_db)):
    db_alumno = db.query(models.Alumno).filter(models.Alumno.email == alumno.email).first()
    if db_alumno:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    nuevo_alumno = models.Alumno(**alumno.dict())
    db.add(nuevo_alumno)
    db.commit()
    db.refresh(nuevo_alumno)
    return nuevo_alumno

# 2. READ: Obtener todos los alumnos
@app.get("/alumno", response_model=List[schemas.AlumnoResponse])
def leer_alumnos(db: Session = Depends(get_db)):
    return db.query(models.Alumno).all()

# 3. READ: Obtener un alumno por ID
@app.get("/alumno/{alumno_id}", response_model=schemas.AlumnoResponse)
def leer_un_alumno(alumno_id: int, db: Session = Depends(get_db)):
    db_alumno = db.query(models.Alumno).filter(models.Alumno.id == alumno_id).first()
    if not db_alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return db_alumno

# 4. UPDATE: Actualizar datos de un alumno
@app.put("/alumno/{alumno_id}", response_model=schemas.AlumnoResponse)
def actualizar_alumno(alumno_id: int, alumno_data: schemas.AlumnoCreate, db: Session = Depends(get_db)):
    db_alumno = db.query(models.Alumno).filter(models.Alumno.id == alumno_id).first()
    if not db_alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    # Actualizamos los campos
    for key, value in alumno_data.dict().items():
        setattr(db_alumno, key, value)
    
    db.commit()
    db.refresh(db_alumno)
    return db_alumno

# 5. DELETE: Borrar un alumno
@app.delete("/alumno/{alumno_id}")
def borrar_alumno(alumno_id: int, db: Session = Depends(get_db)):
    db_alumno = db.query(models.Alumno).filter(models.Alumno.id == alumno_id).first()
    if not db_alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    db.delete(db_alumno)
    db.commit()
    return {"mensaje": f"Alumno con ID {alumno_id} eliminado correctamente"}