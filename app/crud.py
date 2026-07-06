from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from . import models, schemas


# ---------- Employees ----------

def create_employee(db: Session, data: schemas.EmployeeCreate) -> models.Employee:
    employee = models.Employee(**data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_employee(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def list_employees(db: Session, skip: int = 0, limit: int = 100, only_active: bool = False):
    query = db.query(models.Employee)
    if only_active:
        query = query.filter(models.Employee.is_active == 1)
    return query.offset(skip).limit(limit).all()


def update_employee(db: Session, employee_id: int, data: schemas.EmployeeUpdate) -> Optional[models.Employee]:
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int) -> bool:
    employee = get_employee(db, employee_id)
    if not employee:
        return False
    db.delete(employee)
    db.commit()
    return True


# ---------- Vehicles ----------

def create_vehicle(db: Session, data: schemas.VehicleCreate) -> models.Vehicle:
    vehicle = models.Vehicle(**data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def list_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()


# ---------- Trips ----------

def create_trip(db: Session, data: schemas.TripCreate) -> models.Trip:
    trip = models.Trip(**data.model_dump())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


def get_trip(db: Session, trip_id: int) -> Optional[models.Trip]:
    return db.query(models.Trip).filter(models.Trip.id == trip_id).first()


def list_trips(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    driver_id: Optional[int] = None,
    status: Optional[models.TripStatus] = None,
):
    query = db.query(models.Trip)
    if driver_id is not None:
        query = query.filter(models.Trip.driver_id == driver_id)
    if status is not None:
        query = query.filter(models.Trip.status == status)
    return query.order_by(models.Trip.planned_departure.desc()).offset(skip).limit(limit).all()


def update_trip(db: Session, trip_id: int, data: schemas.TripUpdate) -> Optional[models.Trip]:
    trip = get_trip(db, trip_id)
    if not trip:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(trip, field, value)
    db.commit()
    db.refresh(trip)
    return trip


def start_trip(db: Session, trip_id: int) -> Optional[models.Trip]:
    """Отметить фактическое отправление и перевести рейс в статус in_progress."""
    trip = get_trip(db, trip_id)
    if not trip:
        return None
    trip.actual_departure = datetime.utcnow()
    trip.status = models.TripStatus.in_progress
    db.commit()
    db.refresh(trip)
    return trip


def complete_trip(db: Session, trip_id: int) -> Optional[models.Trip]:
    """Отметить фактическое прибытие и перевести рейс в статус completed."""
    trip = get_trip(db, trip_id)
    if not trip:
        return None
    trip.actual_arrival = datetime.utcnow()
    trip.status = models.TripStatus.completed
    db.commit()
    db.refresh(trip)
    return trip


def delete_trip(db: Session, trip_id: int) -> bool:
    trip = get_trip(db, trip_id)
    if not trip:
        return False
    db.delete(trip)
    db.commit()
    return True
