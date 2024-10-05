from fastapi import FastAPI, Depends, HTTPException
import requests

app = FastAPI()

@app.get("/")
def is_alive():
    return {"message": "API Orquestador is alive"}

@app.get("/api_clientes/")
def api_clientes():
    response = requests.get("http://api-clientes-fastapi:8001/")
    return response.json()

@app.get("/api_membresias/")
def api_membresias():
    response = requests.get("http://api-membresias-golang:8002/")
    return response.json()

@app.get("/api_promociones/")
def api_promociones():
    response = requests.get("http://api-promociones-nodejs:8003/")
    return response.json()