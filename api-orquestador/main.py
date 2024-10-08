from fastapi import FastAPI, Depends, HTTPException
import requests
import logging

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Add this after creating the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



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
#API_MEMBRESIAS = "http://localhost:8002"
API_PROMOCIONES = "http://api-promociones-nodejs:8003"


@app.get("/")
def is_alive():
    return {"message": "API Orquestador is alive"}


@app.get("/verificar_membresia/{dni_cliente}")
def verificar_membresia(dni_cliente: str):
    print(f"Verificando membresia de {dni_cliente}")
    response = requests.get(f"{API_CLIENTES}/clientes/real/{dni_cliente}").json()
    status = int(response.get("status", 404))

    promociones_generales = requests.get(f"{API_PROMOCIONES}/promociones").json()
    if status == 404:
        # Si está caducada, la UI procede a solicitar las promociones.
        return {
            "status": "404",
            "message": "Cliente no encontrado",
            "promociones": promociones_generales
        }
    
    elif status == 200:
        # Si la membresía está activa, responde a la UI con un mensaje de confirmación.
        membresia_info = requests.get(f"{API_MEMBRESIAS}/membresias/{dni_cliente}").json()
        if membresia_info["estado"].lower() != "activo":
            promociones_exclusivas = requests.get(f"{API_PROMOCIONES}/promociones_exclusivas/{dni_cliente}").json()
        return {
            **response,
            "membresia": membresia_info,
            "promociones": promociones_generales,
            "promociones_exclusivas": promociones_exclusivas
        }
    else:
        return {
            "status": "500",
            "message": "No se ha podido procesar la solicitud",
            "data": None
        }

@app.post("/cancelar_membresia")
async def cancelar_membresia(body: dict):
    try:
        response = requests.put(f"{API_MEMBRESIAS}/cancelar-membresia/{body['dni']}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error calling membresias API: {str(e)}")
        return {"status": "500", "message": f"Error: {str(e)}"}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"status": "500", "message": "Unexpected server error"}
@app.post("/renovar_membresia")
def renovar_membresia(body: dict):
    response = requests.post(f"{API_MEMBRESIAS}/membresias/", json=body)
    return response.json()
    

"""
INSERT INTO mysql.cliente_real VALUES 
('77777777', 'Hello', 'World', 'hola.mundo@all.edu.pe', true, '2024-09-01 00:00:00');
"""