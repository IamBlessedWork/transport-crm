import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum as SqlEnum,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class EmployeeRole(str, enum.Enum):
    driver = "driver"          # водитель
    dispatcher = "dispatcher"  # диспетчер
    mechanic = "mechanic"      # механик
    manager = "manager"        # менеджер


class TripStatus(str, enum.Enum):
    planned = "planned"        # запланирован
    in_progress = "in_progress"  # в пути
    completed = "completed"    # завершён
    cancelled = "cancelled"    # отменён


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    role = Column(SqlEnum(EmployeeRole), nullable=False, default=EmployeeRole.driver)
    license_number = Column(String(100), nullable=True)  # номер вод. удостоверения
    hired_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)  # 1 = работает, 0 = уволен

    # Рейсы, где этот сотрудник — водитель
    trips = relationship("Trip", back_populates="driver")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), unique=True, nullable=False)
    model = Column(String(100), nullable=True)
    capacity_kg = Column(Float, nullable=True)

    trips = relationship("Trip", back_populates="vehicle")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)

    origin = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)

    planned_departure = Column(DateTime, nullable=False)
    actual_departure = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime, nullable=True)

    distance_km = Column(Float, nullable=True)
    cargo_description = Column(Text, nullable=True)

    status = Column(SqlEnum(TripStatus), default=TripStatus.planned, nullable=False)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    driver = relationship("Employee", back_populates="trips")
    vehicle = relationship("Vehicle", back_populates="trips")
