import random
from datetime import date, timedelta
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import models

def seed_db():
    db = SessionLocal()
    
    # 1. LIMPIEZA TOTAL (Para evitar el error de tablas)
    print("🧹 Limpiando base de datos...")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    # 2. CARGAR 20 EJERCICIOS (El catálogo técnico)
    print("🏋️ Cargando ejercicios...")
    nombres_ejercicios = [
        "Press de Banca", "Sentadillas", "Peso Muerto", "Press Militar", 
        "Remo con Barra", "Dominadas", "Curl de Bíceps", "Press Francés",
        "Estocadas", "Vuelos Laterales", "Press Inclinado", "Fondos de Tríceps",
        "Prensa de Piernas", "Camilla de Cuádriceps", "Remo en Polea", 
        "Face Pulls", "Hip Thrust", "Plancha Abdominal", "Crunch", "Burpees"
    ]
    ejercicios_objetos = []
    for nombre in nombres_ejercicios:
        ej = models.Ejercicio(nombre=nombre)
        db.add(ej)
        ejercicios_objetos.append(ej)
    db.commit()

    # 3. CARGAR 3 PROFESORES
    print("👨‍🏫 Cargando profesores...")
    profe_nombres = ["Giovanni (El Capo)", "Franco", "Lucía"]
    profesores_objetos = []
    for p_nom in profe_nombres:
        profe = models.Profesor(nombre=p_nom)
        db.add(profe)
        profesores_objetos.append(profe)
    db.commit()

    # 4. CARGAR 10 ALUMNOS (Incluyendo a Enzo)
    print("👥 Cargando alumnos...")
    alumnos_data = [
        ("Enzo", "Pérez", "35123456"), ("Bautista", "García", "40987654"),
        ("Martina", "Sánchez", "38111222"), ("Julián", "Álvarez", "42333444"),
        ("Sofía", "Rodríguez", "36555666"), ("Lucas", "López", "39777888"),
        ("Valentina", "Gómez", "37999000"), ("Mateo", "Díaz", "41222333"),
        ("Camila", "Paz", "34444555"), ("Nicolás", "Torres", "43666777")
    ]
    alumnos_objetos = []
    for nom, ape, dni in alumnos_data:
        alu = models.Alumno(
            nombre=nom, apellido=ape, dni=dni, 
            email=f"{nom.lower()}@gym.com", 
            fecha_nacimiento=date(1990, 1, 1),
            objetivo="Ganar masa muscular"
        )
        db.add(alu)
        alumnos_objetos.append(alu)
    db.commit()

    # 5. CARGAR TIPO DE RUTINA (Fuerza por defecto)
    tipo_fuerza = models.TipoRutina(nombre="Hipertrofia/Fuerza")
    db.add(tipo_fuerza)
    db.commit()

    # 6. CARGAR 7 RUTINAS (Con 10 ejercicios cada una)
    print("📋 Generando 7 rutinas de 10 ejercicios cada una...")
    for i in range(7):
        alumno_asignado = random.choice(alumnos_objetos)
        rutina = models.Rutina(
            nombre=f"Rutina de {alumno_asignado.nombre} - Fase {i+1}",
            alumno_id=alumno_asignado.id,
            tipo_rutina_id=tipo_fuerza.id,
            fecha_desde=date.today(),
            fecha_hasta=date.today() + timedelta(days=30),
            vigente=True
        )
        db.add(rutina)
        db.commit()
        db.refresh(rutina)

        # Seleccionar 10 ejercicios aleatorios sin repetir para esta rutina
        ejercicios_seleccionados = random.sample(ejercicios_objetos, 10)
        
        for orden, ej_base in enumerate(ejercicios_seleccionados, 1):
            detalle = models.RutinaEjercicio(
                rutina_id=rutina.id,
                ejercicio_id=ej_base.id,
                orden=orden,
                series=random.choice([3, 4, 5]),
                repeticiones=random.choice(["10", "12", "15", "18"])
            )
            db.add(detalle)
    
    db.commit()
    print("✅ ¡Gimnasio operativo al 100%! Giovanni está orgulloso.")
    db.close()

if __name__ == "__main__":
    seed_db()