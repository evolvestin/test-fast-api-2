from app import models
from app import schemas
from sqlalchemy.orm import Session


def create_resume(db: Session, resume: schemas.ResumeCreate):
    """Функция для создания нового резюме в базе данных."""
    db_resume = models.Resume(candidate_name=resume.candidate_name, file_path=resume.file_path)
    db.add(db_resume)  # Добавляем объект резюме в базу
    db.commit()  # Коммитим изменения в базе данных
    db.refresh(db_resume)  # Обновляем объект резюме с актуальными данными из базы
    return db_resume  # Возвращаем созданное резюме


def get_resumes(db: Session, skip: int = 0, limit: int = 10) -> list:
    """Функция для получения списка резюме с возможностью пропуска и ограничения числа результатов"""
    return db.query(models.Resume).offset(skip).limit(limit).all()  # Возвращаем список резюме с пагинацией


def delete_resume(db: Session, resume_id: int) -> bool:
    """Функция для удаления резюме по его ID"""
    db_resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()  # Ищем резюме по ID
    if db_resume:  # Если резюме найдено
        db.delete(db_resume)  # Удаляем резюме
        db.commit()  # Коммитим изменения в базе данных
        return True
    return False


def rate_resume(db: Session, rating: schemas.RatingCreate):
    "Функция для оценки резюме пользователем"
    db_rating = models.Rating(resume_id=rating.resume_id, user_rating=rating.user_rating)
    db.add(db_rating)  # Добавляем объект оценки в базу данных

    # Обновляем рейтинг резюме после добавления новой оценки
    resume = db.query(models.Resume).filter(models.Resume.id == rating.resume_id).first()
    if resume:  # Если резюме найдено.
        resume.num_ratings += 1  # Увеличиваем количество оценок и пересчитываем средний рейтинг резюме
        resume.rating = ((resume.rating * (resume.num_ratings - 1)) + rating.user_rating) / resume.num_ratings
        db.commit()  # Коммитим изменения в базе данных

    db.refresh(db_rating)  # Обновляем объект оценки с актуальными данными из базы
    return db_rating  # Возвращаем созданную оценку
