from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import models, schemas
from database import engine, get_db

# Crear tablas en la DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gym App Management 2026")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RUTAS DE CONFIGURACIÓN ---

@app.post("/tipo-rutina", response_model=schemas.TipoRutinaResponse, tags=["Config"])
def crear_tipo_rutina(tipo: schemas.TipoRutinaBase, db: Session = Depends(get_db)):
    nuevo = models.TipoRutina(**tipo.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/tipo-rutina", response_model=List[schemas.TipoRutinaResponse], tags=["Config"])
def listar_tipo_rutina(db: Session = Depends(get_db)):
    return db.query(models.TipoRutina).all()

@app.post("/profesor", response_model=schemas.ProfesorResponse, tags=["Personal"])
def crear_profesor(profe: schemas.ProfesorBase, db: Session = Depends(get_db)):
    nuevo = models.Profesor(**profe.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# --- RUTAS DE ALUMNOS ---

@app.post("/alumno", response_model=schemas.AlumnoResponse, tags=["Alumnos"])
def crear_alumno(alumno: schemas.AlumnoCreate, db: Session = Depends(get_db)):
    if db.query(models.Alumno).filter(models.Alumno.email == alumno.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    nuevo = models.Alumno(**alumno.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/alumno", response_model=List[schemas.AlumnoResponse], tags=["Alumnos"])
def listar_alumnos(db: Session = Depends(get_db)):
    return db.query(models.Alumno).all()

# --- RUTAS DE ENTRENAMIENTO ---

@app.post("/ejercicio", response_model=schemas.EjercicioResponse, tags=["Ejercicios"])
def crear_ejercicio(ej: schemas.EjercicioBase, db: Session = Depends(get_db)):
    nuevo = models.Ejercicio(**ej.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/ejercicio", response_model=List[schemas.EjercicioResponse], tags=["Ejercicios"])
def listar_ejercicios(db: Session = Depends(get_db)):
    return db.query(models.Ejercicio).all()

@app.post("/rutina", response_model=schemas.RutinaResponse, tags=["Entrenamiento"])
def crear_rutina(rutina: schemas.RutinaCreate, db: Session = Depends(get_db)):
    # 1. Crear el objeto base de la Rutina
    nueva_rutina = models.Rutina(
        nombre=rutina.nombre,
        tipo_rutina_id=rutina.tipo_rutina_id,
        fecha_desde=rutina.fecha_desde,
        fecha_hasta=rutina.fecha_hasta,
        vigente=rutina.vigente
    )
    db.add(nueva_rutina)
    db.flush() # Esto nos da el ID de la rutina sin terminar la transacción

    # 2. Crear los detalles de cada ejercicio
    for ej_data in rutina.ejercicios:
        detalle = models.RutinaEjercicio(
            rutina_id=nueva_rutina.id,
            ejercicio_id=ej_data.ejercicio_id,
            orden=ej_data.orden,
            series=ej_data.series,
            repeticiones=ej_data.repeticiones
        )
        db.add(detalle)

    db.commit()
    db.refresh(nueva_rutina)
    return nueva_rutina

@app.get("/rutina", response_model=List[schemas.RutinaResponse], tags=["Rutina"])
def listar_rutina(db: Session = Depends(get_db)):
    return db.query(models.Rutina).all()

# --- ASIGNACIONES Y CONSULTA FINAL ---

@app.post("/alumno/{alumno_id}/asignar-rutina/{rutina_id}", tags=["Asignaciones"])
def asignar_rutina_a_alumno(alumno_id: int, rutina_id: int, db: Session = Depends(get_db)):
    alumno = db.query(models.Alumno).filter(models.Alumno.id == alumno_id).first()
    rutina = db.query(models.Rutina).filter(models.Rutina.id == rutina_id).first()

    if not alumno or not rutina:
        raise HTTPException(status_code=404, detail="Alumno o Rutina no encontrados")

    # Si la rutina es vigente, apagamos las anteriores del alumno
    if rutina.vigente:
        for r in alumno.rutinas:
            r.vigente = False

    if rutina not in alumno.rutinas:
        alumno.rutinas.append(rutina)
    
    db.commit()
    return {"mensaje": f"Rutina '{rutina.nombre}' asignada a {alumno.nombre}"}

@app.get("/alumno/{alumno_id}/rutina-vigente", response_model=schemas.RutinaResponse, tags=["Alumnos"])
def obtener_rutina_vigente(alumno_id: int, db: Session = Depends(get_db)):
    alumno = db.query(models.Alumno).filter(models.Alumno.id == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    rutina_vigente = next((r for r in alumno.rutinas if r.vigente), None)
    if not rutina_vigente:
        raise HTTPException(status_code=404, detail="No tiene rutina vigente")

    return rutina_vigente

# --- CRUD: PROFESORES ---

@app.get("/profesor", response_model=List[schemas.ProfesorResponse], tags=["Personal"])
def listar_profesores(db: Session = Depends(get_db)):
    return db.query(models.Profesor).all()

@app.get("/profesor/{id}", response_model=schemas.ProfesorResponse, tags=["Personal"])
def obtener_profesor(id: int, db: Session = Depends(get_db)):
    profe = db.query(models.Profesor).filter(models.Profesor.id == id).first()
    if not profe:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profe

# --- CRUD: ACTIVIDADES (Clases Grupales) ---

@app.post("/actividad", response_model=schemas.ActividadResponse, tags=["Agenda"])
def crear_actividad(actividad: schemas.ActividadCreate, db: Session = Depends(get_db)):
    # Verificamos que el profesor asignado a la clase exista
    profe = db.query(models.Profesor).filter(models.Profesor.id == actividad.profesor_id).first()
    if not profe:
        raise HTTPException(status_code=404, detail="El profesor asignado no existe")
    
    nueva_act = models.Actividad(**actividad.dict())
    db.add(nueva_act)
    db.commit()
    db.refresh(nueva_act)
    return nueva_act

@app.get("/actividad", response_model=List[schemas.ActividadResponse], tags=["Agenda"])
def listar_actividades(db: Session = Depends(get_db)):
    return db.query(models.Actividad).all()

@app.delete("/actividad/{id}", tags=["Agenda"])
def eliminar_actividad(id: int, db: Session = Depends(get_db)):
    act = db.query(models.Actividad).filter(models.Actividad.id == id).first()
    if not act:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    db.delete(act)
    db.commit()
    return {"mensaje": "Actividad eliminada"}