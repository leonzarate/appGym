from fastapi.middleware.cors import CORSMiddleware # IMPORTANTE
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
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

@app.post("/alumnos", response_model=schemas.AlumnoResponse)
def crear_alumno(alumno_data: schemas.AlumnoCreate, db: Session = Depends(get_db)):
    # 1. Verificamos si el email ya existe (para no repetir alumnos)
    existe = db.query(models.Alumno).filter(models.Alumno.email == alumno_data.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Este email ya está registrado.")
    
    # 2. "Cargamos la barra": Creamos el objeto Alumno con los datos recibidos
    nuevo_alumno = models.Alumno(
        nombre=alumno_data.nombre,
        email=alumno_data.email,
        objetivo=alumno_data.objetivo
    )
    
    # 3. Guardamos en la base de datos
    db.add(nuevo_alumno)
    db.commit()
    db.refresh(nuevo_alumno) # Para obtener el ID generado automáticamente
    
    #return "Alumno creado con ID: " + str(nuevo_alumno.id)
    return nuevo_alumno
    

@app.get("/alumnos")
def leer_alumnos(db: Session = Depends(get_db)):
    return db.query(models.Alumno).all()