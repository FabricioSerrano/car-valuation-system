from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from models.reference_model import Reference
from models import base
    
class Brand(base):
    __tablename__ = 'brands'
    
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    active = Column(Boolean, nullable=False, default=True)
    reference_id = Column(Integer, ForeignKey(Reference.id), nullable=False)
