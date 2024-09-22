from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

Base = declarative_base()


class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор резюме
    candidate_name = Column(String, index=True)  # Имя кандидата
    file_path = Column(String)  # Путь до файла с резюме
    rating = Column(Float, default=0.0)  # Средний рейтинг резюме
    num_ratings = Column(Integer, default=0)  # Количество оценок резюме


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор оценки
    resume_id = Column(Integer, ForeignKey('resumes.id'))  # ID резюме, которое оценивается
    user_rating = Column(Float)  # Оценка пользователя
    resume = relationship('Resume', back_populates='ratings')  # Определение отношения между оценками и резюме


Resume.ratings = relationship('Rating', back_populates='resume')  # Определение отношения между резюме и его оценками
