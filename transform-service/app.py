from fastapi import FastAPI
from typing import List
import requests
from urllib.parse import quote
from constants import PERSONAJES_POPULARES_NARUTO as personajes
import environment as E


app = FastAPI()

@app.get('/')
def health():
    """Healthy Transform"""
    return {'status': 'Healthy'}

def obtener_detalle_personaje(nombre: str):
    """
    Función para obtener los detalles de un personaje desde una API externa.

    Args:
        nombre (str): Nombre del personaje a consultar.

    Returns:
        dict: Datos del personaje en formato JSON.
    """
    url = f"{E.EXTRACT_URL_}{quote(nombre)}"
    print(url)
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

@app.get("/clanes_personajes_populares")
async def clanes_personajes_populares() -> dict:
    """
    Endpoint para obtener los personajes populares y agruparlos por clanes (apellidos).

    Returns:
        dict: Un diccionario donde las claves son los apellidos y los valores son listas de nombres de personajes.
    """
    personajes_data = []
    for personaje in personajes:
        try:
            data = obtener_detalle_personaje(personaje)
            if isinstance(data, list) and len(data) > 0:
                personajes_data.append(data[0])
        except requests.exceptions.RequestException as e:
            print(f"Error consultando API para {personaje}: {e}")

    clanes = {}
    for personaje_data in personajes_data:
        full_name = personaje_data.get('name', '')
        names = full_name.split(' ')
        if len(names) > 1:
            apellido = names[-1]
            if apellido not in clanes:
                clanes[apellido] = []
            clanes[apellido].append(full_name)

    return clanes

