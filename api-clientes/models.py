from sqlalchemy import Column, Integer, String, Boolean
from .db import Base
from pydantic import BaseModel

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, nullable=False)
    activo = Column(Boolean, default=True)

Base.metadata.create_all()      # Crear la tabla en la base de datos

class ClienteModel(BaseModel):
    dni: str
    nombre: str
    apellido: str
    email: str
    activo: bool