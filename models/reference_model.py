from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from models import base


class Reference(base):
    __tablename__ = 'references'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    reference_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    active = Column(Boolean, default=True)
