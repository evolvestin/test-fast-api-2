import os
import shutil
from app import crud
from uuid import uuid4
from typing import List
from app import schemas
from app import database
from app.base import base_dir
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, UploadFile, Form


router = APIRouter()  # Создаем объект маршрутизатора


@router.post('/upload/')
def upload_resume(
    candidate_name: str = Form(...),  # Имя кандидата
    file: UploadFile = File(...),  # Загружаемый файл резюме
    db: Session = Depends(database.get_db)  # Зависимость для получения сессии базы данных
):
    """Роут для загрузки нового резюме"""
    if 'uploads' not in os.listdir(base_dir):  # Проверяем, существует ли папка для загрузки файлов
        os.mkdir(base_dir.joinpath('uploads'))  # Если нет, создаем папку

    file_name = uuid4()  # Генерируем уникальное имя для файла
    file_extension = os.path.splitext(file.filename)[1]  # Определяем расширение загружаемого файла
    save_path = base_dir.joinpath('uploads', f'{file_name}{file_extension}')  # Полный путь для сохранения файла

    with open(save_path, 'wb') as new_file:
        shutil.copyfileobj(file.file, new_file)  # Сохраняем файл на сервере

    # Создаем запись резюме в базе данных
    resume = schemas.ResumeCreate(candidate_name=candidate_name, file_path=save_path.as_posix())
    return crud.create_resume(db=db, resume=resume)  # Сохраняем резюме и возвращаем результат


@router.delete('/delete/{resume_id}')
def delete_resume(resume_id: int, db: Session = Depends(database.get_db)):
    """Роут для удаления резюме по его ID"""
    result = crud.delete_resume(db=db, resume_id=resume_id)  # Пытаемся удалить резюме
    if result:
        return {'msg': 'Resume deleted successfully'}  # Успешное удаление
    else:
        return {'msg': 'Resume not found'}  # Резюме не найдено


@router.get('/list/', response_model=List[schemas.Resume])
def list_resumes(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    """Роут для получения списка резюме"""
    return crud.get_resumes(db, skip=skip, limit=limit)  # Получаем и отправляем список резюме


@router.post('/rate/')
def rate_resume(rating: schemas.RatingCreate, db: Session = Depends(database.get_db)):
    """Роут для оценки резюме"""
    return crud.rate_resume(db=db, rating=rating)  # Оцениваем резюме и отправляем результат
