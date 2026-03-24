from pydantic import BaseModel, EmailStr
from datetime import date, time
from typing import List, Optional

# --- TIPO RUTINA ---
class TipoRutinaBase(BaseModel):
    nombre: str

class TipoRutinaResponse(TipoRutinaBase):
    id: int
    class Config:
        from_attributes = True

# --- PROFESOR ---
class ProfesorBase(BaseModel):
    nombre: str
    contacto: Optional[str] = None

class ProfesorCreate(ProfesorBase):
    pass # Se usa para recibir datos en el POST

class ProfesorResponse(ProfesorBase):
    id: int
    class Config:
        from_attributes = True

# --- EJERCICIO ---
class EjercicioBase(BaseModel):
    nombre: str
    video_url: Optional[str] = None
    tips: Optional[str] = None
    profesor_id: int

class EjercicioCreate(EjercicioBase):
    pass  # Se usa para el POST /ejercicio

class EjercicioResponse(EjercicioBase):
    id: int
    class Config:
        from_attributes = True

# --- DETALLE DE EJERCICIO EN RUTINA (La clave del nuevo sistema) ---
class EjercicioEnRutinaResponse(BaseModel):
    orden: int
    series: int
    repeticiones: int
    ejercicio: EjercicioResponse
    class Config:
        from_attributes = True

# --- RUTINA ---
class RutinaResponse(BaseModel):
    id: int
    nombre: str
    vigente: bool
    fecha_desde: date
    fecha_hasta: date
    tipo: Optional[TipoRutinaResponse] # Aquí se usa el esquema que faltaba
    ejercicios_detalle: List[EjercicioEnRutinaResponse]
    class Config:
        from_attributes = True

# --- ALUMNO ---
class AlumnoBase(BaseModel):
    nombre: str
    email: EmailStr
    objetivo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    esta_activo: bool = True

class AlumnoCreate(AlumnoBase):
    pass  # <--- Aquí está el que te faltaba

class AlumnoResponse(AlumnoBase):
    id: int
    rutinas: List[RutinaResponse] = [] # Incluye sus planes de entrenamiento
    class Config:
        from_attributes = True

# --- ACTIVIDAD (Agenda Grupal) ---
class ActividadBase(BaseModel):
    nombre: str
    turno: str
    publico: str
    horario_inicio: time
    horario_fin: time
    profesor_id: int

class ActividadResponse(ActividadBase):
    id: int
    profesor: Optional[ProfesorResponse]
    class Config:
        from_attributes = True

# --- ESQUEMAS PARA CREACIÓN (POST) ---
class EjercicioEnRutinaCreate(BaseModel):
    ejercicio_id: int
    orden: int
    series: int
    repeticiones: int

class RutinaCreate(BaseModel):
    nombre: str
    tipo_rutina_id: int
    fecha_desde: date
    fecha_hasta: date
    vigente: bool = True
    ejercicios: List[EjercicioEnRutinaCreate]

class ActividadCreate(ActividadBase):
    pass