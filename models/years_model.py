from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from models import base

class Year(base):
    __tablename__ = 'years'

    id = Column(String(100), primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    active = Column(Boolean, default=True)