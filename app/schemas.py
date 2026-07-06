from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .models import EmployeeRole, TripStatus


# ---------- Employee ----------

class EmployeeBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    role: EmployeeRole = EmployeeRole.driver
    license_number: Optional[str] = None
    is_active: int = 1


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[EmployeeRole] = None
    license_number: Optional[str] = None
    is_active: Optional[int] = None


class EmployeeOut(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    hired_at: datetime


# ---------- Vehicle ----------

class VehicleBase(BaseModel):
    plate_number: str
    model: Optional[str] = None
    capacity_kg: Optional[float] = None


class VehicleCreate(VehicleBase):
    pass


class VehicleOut(VehicleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Trip ----------

class TripBase(BaseModel):
    driver_id: int
    vehicle_id: Optional[int] = None
    origin: str
    destination: str
    planned_departure: datetime
    distance_km: Optional[float] = None
    cargo_description: Optional[str] = None
    notes: Optional[str] = None


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    status: Optional[TripStatus] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    distance_km: Optional[float] = None
    notes: Optional[str] = None


class TripOut(TripBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: TripStatus
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    created_at: datetime
