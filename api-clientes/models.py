from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session
from db import Base, engine
from pydantic import BaseModel
import time
from datetime import datetime




class Cliente(Base):
    __tablename__ = "cliente_real"

    
    dni = Column(String(50), primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)    
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.now())



class ClienteInvitado(Base):
    __tablename__ = "cliente_invitado"

    dni = Column(String(50), primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)    
    fecha_invitacion = Column(DateTime, default=datetime.now())
    referido_por = Column(String(50), nullable=True)

    



    

time.sleep(10)
Base.metadata.create_all(bind=engine)      # Crear la tabla en la base de datos


def insert_dummy_data():
    session = Session(bind=engine)

    cliente1 = Cliente(dni='77777777', nombre='John', apellido='Doe', email='john.doe@example.com')
    cliente2 = Cliente(dni='99999999', nombre='Jane', apellido='Smith', email='jane.smith@example.com')

    cliente_invitado1 = ClienteInvitado(dni='11111111', nombre='Alice', apellido='Johnson', email='alice.johnson@example.com', referido_por='77777777')
    cliente_invitado2 = ClienteInvitado(dni='22222222', nombre='Bob', apellido='Williams', email='bob.williams@example.com', referido_por='99999999')

    session.add(cliente1)
    session.add(cliente2)
    session.add(cliente_invitado1)
    session.add(cliente_invitado2)

    session.commit()
    session.close()

insert_dummy_data()

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

from sqlalchemy import delete

def truncate_table(db: Session):
    db.execute(delete(ClienteInvitado))
    db.execute(delete(Cliente))
    db.commit()
