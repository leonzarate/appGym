from pydantic import BaseModel, EmailStr
from typing import Optional

# Lo que pedimos cuando alguien se registra
class AlumnoCreate(BaseModel):
    nombre: str
    email: str # Si quieres validar que sea email real, usa EmailStr (requiere: pip install pydantic[email])
    objetivo: Optional[str] = "Mantenimiento"

# Lo que devolvemos (incluye el ID que genera la base de datos)
class AlumnoResponse(AlumnoCreate):
    id: int

    class Config:
        from_attributes = True
