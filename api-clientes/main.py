from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Cliente, ClienteModel, ClienteInvitado,  truncate_table, ClienteInvitadoModel

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


@app.get("/")
def is_alive():
    return {"message": "API Clientes is alive"}


# ------------------- Leer clientes -------------------


@app.get("/clientes/invitado/")
def read_clientes_invitados_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_clientes = db.query(ClienteInvitado).offset(skip).limit(limit).all()
    return {
        "status": "200",
        "message": "Clientes invitados encontrados",
        "data": db_clientes
    }

@app.get("/clientes/real/")
def read_clientes_reales_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_clientes = db.query(Cliente).offset(skip).limit(limit).all()
    return {
        "status": "200",
        "message": "Clientes reales encontrados",
        "data": db_clientes
    }
# ------------------- Leer clientes -------------------


# ------------------- Crear cliente -------------------
# Recibe el cliente por DNI


@app.get("/clientes/real/{dni}")
def read_cliente_real(dni: str, db : Session = Depends(get_db)):
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
            "referido_por": db_cliente.referido_por
        }
    }



@app.put("/clientes/")
def update_cliente( cliente: ClienteModel, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.dni == cliente.dni).first()
    if db_cliente is None:
        return {
            "status": "404",
            "message": "Cliente no encontrado. No se puede actualizar los datos",
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

@app.post("/clientes/delete/{dni}")
def delete_cliente(dni: str, db: Session = Depends(get_db)):
    print(dni)
    db_cliente = db.query(Cliente).filter(Cliente.dni == dni).first()
    if db_cliente is None:
        return {
            "status": "404",
            "message": "Cliente no encontrado",
            "data": None
        }
    db_cliente.activo = False
    db.commit()
    db.refresh(db_cliente)
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
@app.post("/clientes/real/")
def create_cliente(cliente: ClienteModel, db: Session = Depends(get_db)):
    db_cliente = Cliente(dni=cliente.dni, nombre=cliente.nombre, apellido=cliente.apellido, email=cliente.email)

    if db.query(Cliente).filter(Cliente.dni == db_cliente.dni).first() is not None:
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
    
    print(db_cliente)
        
    
    
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




@app.post("/clientes/invitado/")
def create_cliente_invitado(cliente: ClienteInvitadoModel, db: Session = Depends(get_db)):
    
        
    db_cliente_inv = ClienteInvitado(dni=cliente.dni, nombre=cliente.nombre, apellido=cliente.apellido, email=cliente.email,
                                     referido_por=cliente.referido_por)
    

    if  db.query(Cliente).filter(Cliente.dni == db_cliente_inv.dni).first() is not None:
        return {
            "status": "404",
            "message": "Cliente con membresia",
            "data": None
        }
    elif db.query(ClienteInvitado).filter(ClienteInvitado.dni == db_cliente_inv.dni).first() is not None:
        return {
            "status": "400",
            "message": "El cliente ya existe",
            "data": None
        }
    elif db.query(Cliente).filter(Cliente.dni == db_cliente_inv.referido_por).first() is None:
        return {
            "status": "400",
            "message": "El referido no existe",
            "data": None
        }
    elif len(db_cliente_inv.dni) != 8:
        return {
            "status": "400",
            "message": "El DNI debe tener 8 caracteres",
            "data": None
        }
    elif not "@" in db_cliente_inv.email:
        return {
            "status": "400",
            "message": "El email no es válido",
            "data": None
        }



    db.add(db_cliente_inv)
    db.commit()
    db.refresh(db_cliente_inv)
    return {
        "status": "200",
        "message": "Cliente creado",
        "data": {
            "dni": db_cliente_inv.dni,
            "nombre": db_cliente_inv.nombre,
            "apellido": db_cliente_inv.apellido, 
            "email": db_cliente_inv.email,
        }
    }

# ------------------- Crear cliente -------------------

# ------------------- Borrar cliente -------------------

@app.delete("/clientes/")
def delete_clientes(db: Session = Depends(get_db)):
    truncate_table(db)
    return {
        "status": "200",
        "message": "Clientes borrados",
        "data": None
    }