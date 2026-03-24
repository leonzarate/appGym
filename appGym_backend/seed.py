from datetime import date, time
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

def seed():
    db = SessionLocal()
    print("🔥 Borrando base de datos antigua para aplicar nueva estructura...")
    
    try:
        # 1. RESET TOTAL DE TABLAS (Drop y Create)
        # Esto asegura que las nuevas columnas 'orden', 'series' y 'reps' existan en la DB
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("🏗️ Estructura de tablas recreada con éxito.")

        # 2. CARGAR TIPOS DE RUTINA
        tipos = [
            models.TipoRutina(nombre="Hipertrofia"),
            models.TipoRutina(nombre="Fuerza Máxima"),
            models.TipoRutina(nombre="Definición")
        ]
        db.add_all(tipos)
        db.commit()

        # 3. CARGAR PROFESORES (Incluyendo a Giovanni)
        profe_giovanni = models.Profesor(nombre="Giovanni", contacto="Especialista en Powerlifting - Rasgos italianos")
        db.add(profe_giovanni)
        db.commit()

        # 4. CARGAR EJERCICIOS BASE
        ejercicios = [
            models.Ejercicio(nombre="Sentadilla con Barra", video_url="https://youtube.com/s1", tips="Bajar hasta romper el paralelo", profesor_id=profe_giovanni.id),
            models.Ejercicio(nombre="Press de Banca", video_url="https://youtube.com/p1", tips="Retracción escapular obligatoria", profesor_id=profe_giovanni.id),
            models.Ejercicio(nombre="Peso Muerto", video_url="https://youtube.com/pm1", tips="Mantener la barra pegada a las tibias", profesor_id=profe_giovanni.id)
        ]
        db.add_all(ejercicios)
        db.commit()

        # 5. CARGAR ALUMNOS
        enzo = models.Alumno(nombre="Enzo", email="enzo@gym.com", objetivo="Ganar fuerza en básicos", fecha_nacimiento=date(1995, 5, 20))
        db.add(enzo)
        db.commit()

        # 6. CREAR LA RUTINA (Sin los ejercicios todavía)
        rutina_fuerza = models.Rutina(
            nombre="Protocolo Fuerza 5x5",
            fecha_desde=date(2026, 3, 20),
            fecha_hasta=date(2026, 6, 20),
            vigente=True,
            tipo_rutina_id=tipos[1].id # Fuerza Máxima
        )
        db.add(rutina_fuerza)
        db.commit()

        # 7. ASIGNAR EJERCICIOS A LA RUTINA CON ORDEN, SERIES Y REPS
        # Usamos la nueva tabla intermedia detallada
        detalle_1 = models.RutinaEjercicio(
            rutina_id=rutina_fuerza.id,
            ejercicio_id=ejercicios[0].id, # Sentadilla
            orden=1,
            series=5,
            repeticiones=5
        )
        detalle_2 = models.RutinaEjercicio(
            rutina_id=rutina_fuerza.id,
            ejercicio_id=ejercicios[1].id, # Press Banca
            orden=2,
            series=5,
            repeticiones=5
        )
        detalle_3 = models.RutinaEjercicio(
            rutina_id=rutina_fuerza.id,
            ejercicio_id=ejercicios[2].id, # Peso Muerto
            orden=3,
            series=3,
            repeticiones=5
        )
        
        db.add_all([detalle_1, detalle_2, detalle_3])
        
        # 8. VINCULAR RUTINA AL ALUMNO
        enzo.rutinas.append(rutina_fuerza)
        
        db.commit()
        print("✅ ¡Gimnasio cargado! Enzo tiene su rutina 5x5 con orden específico.")

    except Exception as e:
        print(f"❌ Error fatal en el seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()