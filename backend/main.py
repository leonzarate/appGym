from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import backend.models as models
import backend.schemas as schemas
from backend.database import engine
from backend.routers import alumnos, rutinas, ejercicios

app = FastAPI(title="Gym DEL PELA")

# Configuración de CORS para que el Frontend hable con el Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTRO DE RUTAS
app.include_router(alumnos.router)
app.include_router(rutinas.router)
app.include_router(ejercicios.router)

@app.get("/")
def home():
    return {"status": "Gimnasio DEL PELA Operativo 🏋️"}