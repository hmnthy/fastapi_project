import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import timedelta
from .jwt_handler import create_access_token
from .models import predict

# Khởi tạo APIRouter thay vì FastAPI
router = APIRouter()

# Modèle pour les données envoyées via POST
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float = 0.0

# Stockage en mémoire (base de données temporaire)
items_db = []

# Endpoint GET pour récupérer tous les éléments
@router.get("/items", response_model=List[Item])
def get_items():
    return items_db

# Endpoint POST pour ajouter un nouvel élément
@router.post("/items")
def create_item(item: Item):
    items_db.append(item)
    return {"message": "Item created successfully", "item": item}

# Endpoint pour le health check
@router.get("/health_check")
def health_check():
    return {"status": "ok", "message": "API is running smoothly"}

# Endpoint pour appeler l'API externe (DataGouv)
@router.get("/datagouv/datasets")
def get_datasets():
    url = "https://www.data.gouv.fr/api/1/datasets/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "status": "success",
            "datasets": data['data'][:5]
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from DataGouv API: {e}")

# Endpoint pour générer un token JWT
@router.post("/token/")
async def login(username: str, password: str):
    if username == "test" and password == "password":
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

# Endpoint pour faire une prédiction
@router.get("/predict/{value}")
async def make_prediction(value: float):
    prediction = predict(value)
    return {"prediction": prediction}