from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite для старта. Файл базы будет лежать рядом с проектом (crm.db).
SQLALCHEMY_DATABASE_URL = "sqlite:///./crm.db"

# check_same_thread=False нужен только для SQLite при работе с FastAPI (несколько потоков)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency для FastAPI: выдаёт сессию БД и гарантированно закрывает её."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
