import os
from app.models import Base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()  # Загружаем переменные окружения из .env файла
url = os.getenv('DATABASE_URL')  # Получаем URL базы данных из переменных окружения

engine = create_engine(url)  # Создаем движок для подключения к базе данных
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Настраиваем сессию для работы с базой


def init_db():
    """Функция для инициализации базы данных (создания таблиц)"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Функция для получения сессии базы данных"""
    db = Session()  # Создаем новую сессию
    try:
        yield db  # Возвращаем сессию для использования
    finally:
        db.close()  # Закрываем сессию после использования
