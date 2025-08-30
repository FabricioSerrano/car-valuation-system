from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from models import base
from models.brand_model import Brand
from models.reference_model import Reference
from datetime import datetime


class Model(base):
    __tablename__ = 'models'
    
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    active = Column(Boolean, nullable=False, default=True)
    brand_id = Column(Integer, ForeignKey(Brand.id), nullable=False)
