import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String
from datetime import datetime

from app.core.database import Base


class RoleEnum(str, enum.Enum):
    field_officer = "field_officer"
    supervisor = "supervisor"
    zonal_officer = "zonal_officer"
    commissioner = "commissioner"


class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    employee_id = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    ward = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
