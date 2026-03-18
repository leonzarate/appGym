from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "Backend del Gimnasio funcionando. ¡A entrenar!"}

@app.get("/alumnos")
def obtener_alumnos():
    # Esto es un ejemplo, luego vendrá de la base de datos
    return [
        {"id": 1, "nombre": "Franco", "objetivo": "Hipertrofia"},
        {"id": 2, "nombre": "Lucía", "objetivo": "Resistencia"}
    ]
    