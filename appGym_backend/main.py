from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Esto crea las tablas en Supabase si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "Backend del Gimnasio funcionando. ¡FUERZA, SIEMPRE FUREZA!! - Conexión con Supabase lista 🚀"}

@app.get("/alumnos")
def leer_alumnos(db: Session = Depends(get_db)):
    # Ahora pedimos los alumnos reales de la base de datos
    alumnos = db.query(models.Alumno).all()
    return alumnos



