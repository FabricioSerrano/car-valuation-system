from models import base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from models.brand_model import Brand
from models.model_model import Model
from models.years_model import Year
from models.fuel_model import Fuel
from models.reference_model import Reference
from datetime import datetime


class ValueModel(base):
    __tablename__ = 'values'

    id = Column(Integer, index=True, autoincrement=True)
    value = Column(String(500), nullable=False)
    brand_id = Column(Integer, ForeignKey(Brand.id), nullable=False             ,primary_key=True)
    model_id = Column(Integer, ForeignKey(Model.id), nullable=False             ,primary_key=True)
    year_id = Column(String(100), ForeignKey(Year.id), nullable=False           ,primary_key=True)
    fuel_id = Column(Integer, ForeignKey(Fuel.id), nullable=False               ,primary_key=True)
    reference_id = Column(Integer, ForeignKey(Reference.id), nullable=False     ,primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
