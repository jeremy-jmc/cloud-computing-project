from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Cliente, ClienteModel, ClienteReal, ClienteInvitado, ClienteInvitadoModel

app = FastAPI()

@app.get("/")
def is_alive():
    return {"message": "API Clientes is alive"}


# ------------------- Leer clientes -------------------
@app.get("/clientes/")
def read_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_clientes = db.query(Cliente).offset(skip).limit(limit).all()
    return {
        "status": "200",
        "message": "Clientes encontrados",
        "data": db_clientes
    }
@app.get("/clientes/invitado/")
def read_clientes_invitados(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_clientes = db.query(ClienteInvitado).offset(skip).limit(limit).all()
    return {
        "status": "200",
        "message": "Clientes invitados encontrados",
        "data": db_clientes
    }

@app.get("/clientes/real/")
def read_clientes_reales(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_clientes = db.query(ClienteReal).offset(skip).limit(limit).all()
    return {
        "status": "200",
        "message": "Clientes reales encontrados",
        "data": db_clientes
    }
# ------------------- Leer clientes -------------------


# ------------------- Crear cliente -------------------
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

@app.get("/clientes/real/{dni}")
def read_cliente_real(dni: str, db : Session = Depends(get_db)):
    db_cliente = db.query(ClienteReal).filter(ClienteReal.dni == dni).first()
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

@app.get("/clientes/invitado/{dni}")
def read_cliente_invitado(dni: str, db : Session = Depends(get_db)):
    db_cliente = db.query(ClienteInvitado).filter(ClienteInvitado.dni == dni).first()
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
    db_cliente = db.query(ClienteReal).filter(ClienteReal.dni == dni).first()
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








# ------------------- Crear cliente -------------------

def create_cliente(cliente: ClienteModel, db: Session):
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


@app.post("/clientes/real/")
def create_cliente_real(cliente: ClienteModel, db: Session = Depends(get_db)):
    response = create_cliente(cliente, db)
    if response["status"] != "200":
        return response
            
    db_cliente_real = ClienteReal(dni=response["data"]["dni"], activo=True)

    db.add(db_cliente_real)
    db.commit()
    db.refresh(db_cliente_real)

@app.post("/clientes/invitado/")
def create_cliente_invitado(cliente: ClienteInvitadoModel, db: Session = Depends(get_db)):
    
    ClienteM = ClienteModel(dni=cliente.dni, nombre=cliente.nombre, apellido=cliente.apellido, email=cliente.email)
    response = create_cliente(ClienteM, db)


    if response["status"] != "200":
        return response
            
    db_cliente_inv = ClienteInvitadoModel(dni=response["data"]["dni"], activo=True)

    db.add(db_cliente_inv)
    db.commit()
    db.refresh(db_cliente_inv)

# ------------------- Crear cliente -------------------