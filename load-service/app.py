import csv
import requests
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import StreamingResponse
from typing import Dict, List
from io import StringIO
import environment as E

app = FastAPI()


def obtener_clanes_personajes() -> Dict[str, List[str]]:
    """
    Obtiene los clanes y sus miembros desde otra API.

    Returns:
        dict: Un diccionario donde las claves son los nombres de los clanes
              y los valores son listas de nombres de personajes.
    """
    try:
        response = requests.get(E.API_URL_)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener clanes y personajes: {str(e)}")

def exportar_clanes_a_csv(clanes: Dict[str, List[str]]) -> str:
    """
    Exporta la lista de clanes y sus miembros a un archivo CSV en memoria.

    Args:
        clanes (dict): Un diccionario donde las claves son los nombres de los clanes
                       y los valores son listas de nombres de personajes.

    Returns:
        str: Contenido del archivo CSV en formato texto.
    """
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Clan', 'Personajes'])
    for clan, miembros in clanes.items():
        for personaje in miembros:
            writer.writerow([clan, personaje])
    csv_content = output.getvalue()
    output.close()
    return csv_content

@app.get('/')
def health():
    """Healthy Load"""
    return {'status': 'Healthy'}

@app.get("/exportar_csv")
async def exportar_csv(response: Response):
    """
    Endpoint para exportar la lista de clanes y sus miembros a un archivo CSV.

    Parameters:
        response (Response): Objeto de respuesta FastAPI.

    Returns:
        StreamingResponse: Respuesta de transmisión con el contenido del archivo CSV.
    """
    try:
        clanes = obtener_clanes_personajes()
        csv_content = exportar_clanes_a_csv(clanes)
        response.headers["Content-Disposition"] = "attachment; filename=clanes_personajes.csv"
        return StreamingResponse(iter([csv_content]), media_type="text/csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al exportar CSV: {str(e)}")


