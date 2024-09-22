import pytest
from app.main import app
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.database import Base, get_db
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


def override_get_db():
    """Переопределяем зависимость get_db для использования тестовой базы данных"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создаем тестовую базу данных SQLite
SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='module', autouse=True)
def create_test_db():
    """Создаем таблицы в тестовой базе данных"""
    Base.metadata.create_all(bind=engine)
    yield engine  # Возвращаем объект engine, чтобы можно было использовать его в тестах
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='module')
def db_session(create_test_db):
    connection = create_test_db.connect()  # Получаем соединение с тестовой базой данных
    session = Session(bind=connection)  # Привязываем сессию к соединению
    yield session
    session.close()
    connection.close()


@pytest.fixture(scope='module')
def client():
    """Клиент для тестирования"""
    with TestClient(app) as app_client:
        yield app_client
