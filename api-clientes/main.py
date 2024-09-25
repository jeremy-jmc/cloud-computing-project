from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from .models import Cliente, ClienteModel

app = FastAPI()


# Recibe el cliente por DNI
@app.get("/clientes/{dni}")
def read_cliente(dni: str, db : Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.dni == dni).first()
    if db_cliente is None:
        return {
            "status": "404",
            "message": "Cliente no encontrado",
            "data": None
        }
        
    return {
        "status": "200",
        "message": "Cliente encontrado",
        "data": {
            "dni": db_cliente.dni,
            "nombre": db_cliente.nombre,
            "apellido": db_cliente.apellido, 
            "email": db_cliente.email,
        }
    }

@app.put("/clientes/{dni}")
def update_cliente(dni: str, cliente: ClienteModel, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.dni == dni).first()
    if db_cliente is None:
        return {
            "status": "404",
            "message": "Cliente no encontrado",
            "data": None
        }
    db_cliente.nombre = cliente.nombre
    db_cliente.apellido = cliente.apellido
    db_cliente.email = cliente.email
    db.commit()
    db.refresh(db_cliente)
    return {
        "status": "200",
        "message": "Cliente actualizado",
        "data": {
            "dni": db_cliente.dni,
            "nombre": db_cliente.nombre,
            "apellido": db_cliente.apellido, 
            "email": db_cliente.email,
        }
    }

@app.put("/clientes/{dni}")
def delete_cliente(dni: str, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.dni == dni).first()
    if db_cliente is None:
        return {
            "status": "404",
            "message": "Cliente no encontrado",
            "data": None
        }
    db_cliente.activo = False
    db.commit()
    return {
        "status": "200",
        "message": "Cliente desactivado",
        "data": {
            "dni": db_cliente.dni,
            "nombre": db_cliente.nombre,
            "apellido": db_cliente.apellido, 
            "email": db_cliente.email,
        }
    }



@app.post("/clientes/")
def create_cliente(cliente: ClienteModel, db: Session = Depends(get_db)):
    db_cliente = Cliente(dni=cliente.dni, nombre=cliente.nombre, apellido=cliente.apellido, email=cliente.email)
    if db.query(Cliente).filter(Cliente.dni == db_cliente.dni).first() :
        return {
            "status": "400",
            "message": "El cliente ya existe",
            "data": None
        }
    elif len(db_cliente.dni) != 8:
        return {
            "status": "400",
            "message": "El DNI debe tener 8 caracteres",
            "data": None
        }
    elif not "@" in db_cliente.email:
        return {
            "status": "400",
            "message": "El email no es válido",
            "data": None
        }
    
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return {
        "status": "200",
        "message": "Cliente creado",
        "data": {
            "dni": db_cliente.dni,
            "nombre": db_cliente.nombre,
            "apellido": db_cliente.apellido, 
            "email": db_cliente.email,
        }
    }