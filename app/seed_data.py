"""
Скрипт первоначального заполнения БД (seed).

Запуск (из папки crm_app, после того как установлены зависимости):
    python -m app.seed_data

Добавляет 20 водителей + 20 машин (украинская регистрация) и связывает
их между собой 1-в-1 по порядку из списка.

Скрипт идемпотентный: если сотрудник с таким ФИО или машина с таким
гос. номером уже есть в базе — запись пропускается, а не дублируется.
"""

from .database import SessionLocal, engine, Base
from . import models

# (ФИО, телефон, марка фуры, гос. номер)
DRIVERS_DATA = [
    ("Коваленко Андрей Николаевич", "+380 67 123-45-67", "DAF XF 105", "AA 4321 HX"),
    ("Шевченко Богдан Игоревич", "+380 50 234-56-78", "Volvo FH12", "BH 8899 EE"),
    ("Мельник Сергей Витальевич", "+380 93 345-67-89", "MAN TGX", "AE 5501 KM"),
    ("Ткаченко Дмитрий Александрович", "+380 68 456-78-90", "Scania R420", "AX 1294 BC"),
    ("Кравченко Александр Петрович", "+380 95 567-89-01", "Mercedes Actros", "BC 7744 HA"),
    ("Олейник Иван Сергеевич", "+380 63 678-90-12", "Renault Magnum", "BX 0023 BO"),
    ("Полищук Виталий Владимирович", "+380 97 789-01-23", "DAF XF 106", "AI 9481 CT"),
    ("Бондаренко Максим Анатольевич", "+380 50 890-12-34", "Volvo FH16", "KA 3322 EX"),
    ("Козак Юрий Михайлович", "+380 66 901-23-45", "MAN TGA", "BM 6152 II"),
    ("Мороз Артем Денисович", "+380 73 012-34-56", "Scania Streamline", "CE 4411 AT"),
    ("Лысенко Роман Олегович", "+380 98 123-98-76", "Iveco Stralis", "AB 7099 HT"),
    ("Руденко Николай Григорьевич", "+380 50 234-87-65", "DAF CF", "AO 5412 CB"),
    ("Петренко Вадим Юрьевич", "+380 67 345-76-54", "Volvo FM", "AC 1188 EK"),
    ("Савченко Евгений Васильевич", "+380 93 456-65-43", "Mercedes Axor", "AM 3940 BX"),
    ("Кириченко Илья Алексеевич", "+380 66 567-54-32", "MAN TGS", "BI 8821 PP"),
    ("Волков Владислав Эдуардович", "+380 68 678-43-21", "Scania R500", "BE 0755 KX"),
    ("Соколов Олег Николаевич", "+380 95 789-32-10", "Renault Premium", "AX 4590 EO"),
    ("Панченко Тарас Степанович", "+380 63 890-21-09", "DAF XF 95", "BB 1313 MM"),
    ("Семенюк Василий Ярославович", "+380 97 901-10-98", "Volvo FH", "AT 6077 HA"),
    ("Марченко Игорь Константинович", "+380 50 012-09-87", "MAN TGX", "CH 9142 PI"),
]


def seed():
    # Создаём таблицы, если их ещё нет (на случай запуска seed до старта сервера)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    added_employees = 0
    added_vehicles = 0

    try:
        for full_name, phone, truck_model, plate_number in DRIVERS_DATA:
            # --- машина ---
            vehicle = (
                db.query(models.Vehicle)
                .filter(models.Vehicle.plate_number == plate_number)
                .first()
            )
            if not vehicle:
                vehicle = models.Vehicle(plate_number=plate_number, model=truck_model)
                db.add(vehicle)
                db.flush()  # получить vehicle.id, не коммитя транзакцию целиком
                added_vehicles += 1

            # --- водитель ---
            employee = (
                db.query(models.Employee)
                .filter(models.Employee.full_name == full_name)
                .first()
            )
            if not employee:
                employee = models.Employee(
                    full_name=full_name,
                    phone=phone,
                    role=models.EmployeeRole.driver,
                    is_active=1,
                )
                db.add(employee)
                added_employees += 1

        db.commit()
        print(f"Готово: добавлено {added_employees} водителей и {added_vehicles} машин.")
        print("Записи, которые уже были в базе (по ФИО / гос. номеру), пропущены.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
