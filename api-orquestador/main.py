from fastapi import FastAPI, Depends, HTTPException
import requests
import logging

app = FastAPI()


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

API_CLIENTES = "http://api-clientes-fastapi:8001"
API_MEMBRESIAS = "http://api-membresias-golang:8002"
API_PROMOCIONES = "http://api-promociones-nodejs:8003"

@app.get("/")
def is_alive():
    return {"message": "API Orquestador is alive"}

@app.get("/verificar_membresia/{dni_cliente}")
def verificar_membresia(dni_cliente: str):
    print(f"Verificando membresia de {dni_cliente}")
    response = requests.get(f"{API_CLIENTES}/clientes/real/{dni_cliente}").json()
    status = int(response.get("status", 404))

    if status == 404:
        # Si está caducada, la UI procede a solicitar las promociones.
        return requests.get(f"{API_PROMOCIONES}/promociones").json()
    elif status == 200:
        # Si la membresía está activa, responde a la UI con un mensaje de confirmación.
        return response
    else:
        return {
            "status": "500",
            "message": "No se ha podido procesar la solicitud",
            "data": None
        }

"""
INSERT INTO mysql.cliente_real VALUES 
('77777777', 'Hello', 'World', 'hola.mundo@all.edu.pe', true, '2024-09-01 00:00:00');
"""