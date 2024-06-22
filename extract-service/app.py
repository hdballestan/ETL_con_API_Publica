import requests
import urllib.parse
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import environment as E

app = FastAPI()

class Character(BaseModel):
    id: int
    name: str
    birthdate: Optional[str] = None
    bloodType: Optional[str] = None
    first_jutsu: Optional[str] = None

@app.get('/')
def health():
    """Healthy Extract"""
    return {'status': 'Healthy'}

@app.get("/extract", response_model=List[Character])
def extract(name: str = Query(..., description="Name of the character to search for")):
    """
    Extracts character data from an external API based on the provided name.

    This endpoint performs a search by name using an external API defined in the environment variables.
    The API response is expected to contain character data that matches the provided name.
    The relevant information is extracted and returned as a list of Character models.

    Parameters:
        name (str): Name of the character to search for.

    Returns:
        List[Character]: A list of characters that match the provided name with the following details:
            - id (int): The unique identifier of the character.
            - name (str): The name of the character.
            - birthdate (Optional[str]): The birthdate of the character, if available.
            - bloodType (Optional[str]): The blood type of the character, if available.
            - first_jutsu (Optional[str]): The first jutsu listed for the character, if available.

    Raises:
        HTTPException: If there is an error fetching data from the external API or if
        any unexpected error occurs during the data processing.
    """
    try:
        encoded_name = urllib.parse.quote(name)
        url = f"{E.API_SEARCH_}?name={encoded_name}"
        headers = {'accept': 'application/json'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            data = [data]

        characters = []
        for char_data in data:
            char_id = char_data.get('id')
            char_name = char_data.get('name')
            personal_info = char_data.get('personal', {})
            char_birthdate = personal_info.get('birthdate')
            char_bloodType = personal_info.get('bloodType')
            jutsu_list = char_data.get('jutsu', [])

            # Tomar el primer jutsu de la lista, si existe
            first_jutsu = jutsu_list[0] if jutsu_list else None

            # Crear el objeto Character y añadirlo a la lista
            character = Character(
                id=char_id,
                name=char_name,
                birthdate=char_birthdate,
                bloodType=char_bloodType,
                first_jutsu=first_jutsu
            )
            characters.append(character)

        return characters

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


