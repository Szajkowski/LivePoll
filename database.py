from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root@localhost/livepoll"

engine = create_engine(
    DATABASE_URL,
    echo=True,          # loguje zapytania SQL
    future=True
)
"""
Obiekt silnika SQLAlchemy używany do połączeń z bazą danych MySQL.

:type: sqlalchemy.Engine
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
Fabryka sesji SQLAlchemy do tworzenia instancji sesji bazy danych.

:type: sqlalchemy.orm.sessionmaker
"""

Base = declarative_base()
"""
Podstawowa klasa bazowa dla modeli SQLAlchemy.

:type: sqlalchemy.orm.decl_api.DeclarativeMeta
"""

def get_db():
    """
    Zwraca sesję bazy danych dla zależności FastAPI.

    Funkcja generatora używana z Depends, aby automatycznie otworzyć
    i zamknąć sesję bazy danych w ramach obsługi żądania HTTP.

    :yield: Sesja bazy danych SQLAlchemy.
    :rtype: sqlalchemy.orm.Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
