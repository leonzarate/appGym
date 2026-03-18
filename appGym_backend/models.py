from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Alumno(Base):
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, index=True)
    esta_activo = Column(Boolean, default=True)
    objetivo = Column(String) # Ej: "Perder peso", "Ganar músculo"
    