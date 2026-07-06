from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

# Создаём таблицы при старте (для прототипа на SQLite этого достаточно;
# в проде лучше использовать миграции Alembic)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Transport CRM API",
    description="Модуль: сотрудники и логирование рейсов",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"status": "ok", "service": "transport-crm"}


# ==================== EMPLOYEES ====================

@app.post("/employees/", response_model=schemas.EmployeeOut, tags=["employees"])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)


@app.get("/employees/", response_model=List[schemas.EmployeeOut], tags=["employees"])
def list_employees(
    skip: int = 0,
    limit: int = 100,
    only_active: bool = False,
    db: Session = Depends(get_db),
):
    return crud.list_employees(db, skip=skip, limit=limit, only_active=only_active)


@app.get("/employees/{employee_id}", response_model=schemas.EmployeeOut, tags=["employees"])
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return employee


@app.patch("/employees/{employee_id}", response_model=schemas.EmployeeOut, tags=["employees"])
def update_employee(employee_id: int, data: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    employee = crud.update_employee(db, employee_id, data)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return employee


@app.delete("/employees/{employee_id}", tags=["employees"])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_employee(db, employee_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return {"deleted": True}


# ==================== VEHICLES ====================

@app.post("/vehicles/", response_model=schemas.VehicleOut, tags=["vehicles"])
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(db, vehicle)


@app.get("/vehicles/", response_model=List[schemas.VehicleOut], tags=["vehicles"])
def list_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_vehicles(db, skip=skip, limit=limit)


# ==================== TRIPS ====================

@app.post("/trips/", response_model=schemas.TripOut, tags=["trips"])
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db)):
    driver = crud.get_employee(db, trip.driver_id)
    if not driver:
        raise HTTPException(status_code=400, detail="Указанный водитель не найден")
    return crud.create_trip(db, trip)


@app.get("/trips/", response_model=List[schemas.TripOut], tags=["trips"])
def list_trips(
    skip: int = 0,
    limit: int = 100,
    driver_id: Optional[int] = None,
    status: Optional[models.TripStatus] = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.list_trips(db, skip=skip, limit=limit, driver_id=driver_id, status=status)


@app.get("/trips/{trip_id}", response_model=schemas.TripOut, tags=["trips"])
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = crud.get_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Рейс не найден")
    return trip


@app.patch("/trips/{trip_id}", response_model=schemas.TripOut, tags=["trips"])
def update_trip(trip_id: int, data: schemas.TripUpdate, db: Session = Depends(get_db)):
    trip = crud.update_trip(db, trip_id, data)
    if not trip:
        raise HTTPException(status_code=404, detail="Рейс не найден")
    return trip


@app.post("/trips/{trip_id}/start", response_model=schemas.TripOut, tags=["trips"])
def start_trip(trip_id: int, db: Session = Depends(get_db)):
    """Отметить фактический выезд машины в рейс."""
    trip = crud.start_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Рейс не найден")
    return trip


@app.post("/trips/{trip_id}/complete", response_model=schemas.TripOut, tags=["trips"])
def complete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Отметить завершение рейса (фактическое прибытие)."""
    trip = crud.complete_trip(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Рейс не найден")
    return trip


@app.delete("/trips/{trip_id}", tags=["trips"])
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_trip(db, trip_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Рейс не найден")
    return {"deleted": True}
