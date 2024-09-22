from app import routers
from app import database
from fastapi import FastAPI


app = FastAPI()  # Создаем экземпляр FastAPI приложения
database.init_db()  # Инициализируем базу данных (создаем таблицы если их не существует)
app.include_router(routers.router)  # Подключаем роуты приложения
