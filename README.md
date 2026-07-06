# Transport CRM — модуль "Сотрудники и рейсы"

Минимальный рабочий бэкенд на **FastAPI + SQLAlchemy + SQLite**.

 Структура
```
crm_app/
├── app/
│   ├── __init__.py
│   ├── database.py   # подключение к SQLite
│   ├── models.py     # таблицы: Employee, Vehicle, Trip
│   ├── schemas.py     # Pydantic-схемы для API
│   ├── crud.py        # функции работы с БД
│   └── main.py        # FastAPI-приложение и роуты
├── requirements.txt
└── README.md
```

 Запуск
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

После запуска:
- API: http://127.0.0.1:8000
- Автодокументация (Swagger): http://127.0.0.1:8000/docs

БД (`crm.db`) создастся автоматически при первом старте в той же папке.

 Что уже создано

 Сотрудники (`/employees/`)
- создание, список, получение по id, обновление, удаление
- роли: `driver`, `dispatcher`, `mechanic`, `manager`
- флаг `is_active` — работает / уволен

 Транспорт (`/vehicles/`)
- создание и список машин (гос. номер, модель, грузоподъёмность)

 Рейсы (`/trips/`)
- создание рейса (с привязкой к водителю и, опционально, к машине)
- список с фильтрами по водителю и статусу
- статусы: `planned → in_progress → completed` (или `cancelled`)
- отдельные эндпоинты `/trips/{id}/start` и `/trips/{id}/complete` —
  фиксируют фактическое время выезда/прибытия и меняют статус
- проверка: нельзя создать рейс на несуществующего водителя

 Пример запроса (curl)

Создать сотрудника:
```bash
curl -X POST http://127.0.0.1:8000/employees/ \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Иван Петров","phone":"+380501234567","role":"driver","license_number":"AB123456"}'
```

Создать рейс:
```bash
curl -X POST http://127.0.0.1:8000/trips/ \
  -H "Content-Type: application/json" \
  -d '{"driver_id":1,"origin":"Одесса","destination":"Киев","planned_departure":"2026-07-10T08:00:00"}'
```

 Заполнение тестовыми данными

В комплекте есть `app/seed_data.py` — заполняет базу 20 водителями и
20 машинами (украинская регистрация) 

```bash
python -m app.seed_data
```

Скрипт идемпотентный: повторный запуск не создаст дубликаты (проверка
идёт по ФИО водителя и по гос. номеру машины).



Модель сотрудника пока не хранит "закреплённую" машину напрямую —
связь водитель↔машина фиксируется на уровне конкретного рейса
(`Trip.driver_id` + `Trip.vehicle_id`).


- добавить JWT-аутентификацию для API
- перейти с create_all на Alembic-миграции (понадобится при переходе с SQLite на PostgreSQL/MySQL)
- сделать отчёты: пробег по водителю/машине за период, статистика по статусам рейсов
- уведомления диспетчеру, если рейс не стартовал вовремя
