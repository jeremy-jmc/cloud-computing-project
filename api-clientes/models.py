from sqlalchemy import Column, Integer, String, Boolean
from db import Base, engine
from pydantic import BaseModel

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String(50), unique=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)      # Crear la tabla en la base de datos

class ClienteModel(BaseModel):
    dni: str
    nombre: str
    apellido: str
    email: str
    activo: bool