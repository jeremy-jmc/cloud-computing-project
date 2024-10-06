from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
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

    



    

time.sleep(10)
Base.metadata.create_all(bind=engine)      # Crear la tabla en la base de datos

class ClienteModel(BaseModel):
    dni: str
    nombre: str
    apellido: str
    email: str




# Truncate tables

from sqlalchemy.orm import Session
from sqlalchemy import delete

def truncate_table(db: Session):
    db.execute(delete(ClienteInvitado))
    db.execute(delete(Cliente))
    db.commit()
