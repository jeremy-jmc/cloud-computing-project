from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from db import Base, engine
from pydantic import BaseModel
import time
from datetime import datetime

class Cliente(Base):
    __tablename__ = "cliente"

    dni = Column(String(50), primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "cliente",
        "polymorphic_on": dni
    }


class ClienteReal(Base):
    __tablename__ = "cliente_real"

    
    dni = Column(String(50), ForeignKey("cliente.dni"), primary_key=True, index=True)    
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.now())

    __mapper_args__ = {
        "polymorphic_identity": "cliente_real"
    }

class ClienteInvitado(Base):
    __tablename__ = "cliente_invitado"

    dni = Column(String(50), ForeignKey("cliente.dni"), primary_key=True, index=True)
    fecha_invitacion = Column(DateTime, default=datetime.now())
    referido_por = Column(String(50)) # DNI del cliente que lo refirio

    _mapper_args = {
        "polymorphic_identity": "cliente_invitado"
    }



    

time.sleep(10)
Base.metadata.create_all(bind=engine)      # Crear la tabla en la base de datos

class ClienteModel(BaseModel):
    dni: str
    nombre: str
    apellido: str
    email: str

class ClienteInvitadoModel(BaseModel):
    dni: str
    nombre: str
    apellido: str
    email: str
    referido_por: str

# Truncate tables

from sqlalchemy.orm import Session
from db import get_db
from models import Cliente, ClienteReal, ClienteInvitado
from sqlalchemy import delete

def truncate_table(db: Session):
    db.execute(delete(ClienteReal))
    db.execute(delete(ClienteInvitado))
    db.execute(delete(Cliente))
    db.commit()
