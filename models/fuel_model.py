from models import base
from sqlalchemy import Column, Integer, String


class Fuel(base):
    __tablename__ = 'fuels'
    
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False, unique=True)
