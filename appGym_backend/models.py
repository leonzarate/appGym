from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

class Alumno(Base):
    __tablename__ = "alumno"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True) # Nuevo campo
    esta_activo = Column(Boolean, default=True)
    objetivo = Column(String, nullable=True)
