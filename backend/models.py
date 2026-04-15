from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum, Time, Table
from sqlalchemy.orm import relationship
import enum
from backend.database import Base

# --- TABLA INTERMEDIA ALUMNO-RUTINA (Sigue siendo simple) ---
alumno_rutina = Table(
    "alumno_rutina",
    Base.metadata,
    Column("alumno_id", Integer, ForeignKey("alumno.id"), primary_key=True),
    Column("rutina_id", Integer, ForeignKey("rutina.id"), primary_key=True)
)

# --- ENUMS ---
class Turno(enum.Enum):
    manana = "manana"
    tarde = "tarde"

class Publico(enum.Enum):
    mixto = "mixto"
    masculino = "masculino"
    femenino = "femenino"

# --- CLASE INTERMEDIA RUTINA-EJERCICIO (LA QUE CAUSA EL ERROR) ---
class RutinaEjercicio(Base):
    __tablename__ = "rutina_ejercicio"
    rutina_id = Column(Integer, ForeignKey("rutina.id"), primary_key=True)
    ejercicio_id = Column(Integer, ForeignKey("ejercicio.id"), primary_key=True)
    orden = Column(Integer, default=1)
    series = Column(Integer)
    repeticiones = Column(Integer)

    # Relación para acceder al objeto ejercicio desde la rutina
    ejercicio = relationship("Ejercicio")

# --- MODELOS PRINCIPALES ---

class TipoRutina(Base):
    __tablename__ = "tipo_rutina"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    rutinas = relationship("Rutina", back_populates="tipo")

class Profesor(Base):
    __tablename__ = "profesor"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    contacto = Column(String)
    actividades = relationship("Actividad", back_populates="profesor")
    ejercicios_creados = relationship("Ejercicio", back_populates="profesor_editor")

class Alumno(Base):
    __tablename__ = "alumno"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    dni = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    fecha_nacimiento = Column(Date)
    esta_activo = Column(Boolean, default=True)
    objetivo = Column(String)
    rutinas = relationship("Rutina", secondary=alumno_rutina, back_populates="alumnos")

class Ejercicio(Base):
    __tablename__ = "ejercicio"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    video_url = Column(String)
    tips = Column(String)
    profesor_id = Column(Integer, ForeignKey("profesor.id"))
    profesor_editor = relationship("Profesor", back_populates="ejercicios_creados")

class Rutina(Base):
    __tablename__ = "rutina"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    fecha_desde = Column(Date)
    fecha_hasta = Column(Date)
    vigente = Column(Boolean, default=True)
    tipo_rutina_id = Column(Integer, ForeignKey("tipo_rutina.id"))
    
    tipo = relationship("TipoRutina", back_populates="rutinas")
    alumnos = relationship("Alumno", secondary=alumno_rutina, back_populates="rutinas")
    # RELACIÓN CLAVE: apunta a la clase RutinaEjercicio
    ejercicios = relationship("RutinaEjercicio", cascade="all, delete-orphan")
    alumno_id = Column(Integer, ForeignKey("alumno.id")) # Debe coincidir con el nombre de tabla 'alumnos'


class Actividad(Base):
    __tablename__ = "actividad"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    turno = Column(Enum(Turno))
    publico = Column(Enum(Publico))
    horario_inicio = Column(Time)
    horario_fin = Column(Time)
    profesor_id = Column(Integer, ForeignKey("profesor.id"))
    profesor = relationship("Profesor", back_populates="actividades")
