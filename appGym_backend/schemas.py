from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

# Base común
class AlumnoBase(BaseModel):
    nombre: str
    email: EmailStr
    fecha_nacimiento: Optional[date] = None
    esta_activo: Optional[bool] = True
    objetivo: Optional[str] = None

# Para crear (hereda de Base)
class AlumnoCreate(AlumnoBase):
    pass

# Para la respuesta del API (incluye el ID)
class AlumnoResponse(AlumnoBase):
    id: int

    class Config:
        from_attributes = True

# Para crear y mostrar rutinas
class RutinaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RutinaCreate(RutinaBase):
    pass

class RutinaResponse(RutinaBase):
    id: int

    class Config:
        from_attributes = True