import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Creamos el motor de la base de datos
engine = create_engine(DATABASE_URL)

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

# Reset de la base de datos (para desarrollo)
def reset_database():

    # 2. Borrar todo lo existente
    Base.metadata.drop_all(engine)
    print("Tablas borradas.")

    # 3. Crear las tablas desde cero
    Base.metadata.create_all(engine)
    print("Tablas creadas.")

