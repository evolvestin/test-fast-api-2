from pydantic import BaseModel


class ResumeBase(BaseModel):
    """Базовая схема для резюме"""
    candidate_name: str  # Имя кандидата


class ResumeCreate(ResumeBase):
    """Схема для создания нового резюме"""
    file_path: str  # Путь к файлу резюме.


class Resume(ResumeBase):
    """Схема для представления резюме"""
    id: int  # Уникальный идентификатор резюме
    rating: float  # Средний рейтинг резюме
    num_ratings: int  # Количество оценок резюме

    class Config:
        orm_mode = True  # Включаем поддержку работы с объектами ORM


class RatingCreate(BaseModel):
    """Схема для создания новой оценки"""
    resume_id: int  # ID резюме
    user_rating: float  # Оценка пользователя
