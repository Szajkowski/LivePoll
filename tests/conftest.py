# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

# --- In-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Tworzymy tabele przed sesją testową
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# --- Fixture dla sesji DB
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


# --- Podmiana get_db w FastAPI
@pytest.fixture(scope="function", autouse=True)
def override_get_db(monkeypatch, db_session):
    def _get_db():
        try:
            yield db_session
        finally:
            pass

    monkeypatch.setattr("database.get_db", _get_db)


# --- TestClient
@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c
