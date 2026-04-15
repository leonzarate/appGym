import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Creamos el motor de la base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c statement_timeout=30000"}, # Opcional: timeout de 30s
    pool_pre_ping=True # Verifica que la conexión esté viva antes de usarla
)

# Creamos una sesión (para hacer consultas)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta será la clase base para nuestros modelos
Base = declarative_base()

# Función para obtener la base de datos en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


