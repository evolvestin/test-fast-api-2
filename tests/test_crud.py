from app import crud, schemas
from app.models import Resume


def test_create_resume(db_session):
    resume_data = schemas.ResumeCreate(candidate_name='Test Candidate', file_path='/path/to/resume')
    resume = crud.create_resume(db_session, resume_data)
    assert resume.candidate_name == 'Test Candidate'
    assert resume.file_path == '/path/to/resume'


def test_get_resumes(db_session):
    resumes = crud.get_resumes(db_session, skip=0, limit=10)
    assert isinstance(resumes, list)
    assert len(resumes) >= 1


def test_delete_resume(db_session):
    resume_data = schemas.ResumeCreate(candidate_name='Candidate to Delete', file_path='/path/to/delete')
    resume = crud.create_resume(db_session, resume_data)
    deleted = crud.delete_resume(db_session, resume.id)
    assert deleted is True


def test_rate_resume(db_session):
    resume_data = schemas.ResumeCreate(candidate_name='Candidate to Rate', file_path='/path/to/rate')
    resume = crud.create_resume(db_session, resume_data)
    rating_data = schemas.RatingCreate(resume_id=resume.id, user_rating=4.0)
    crud.rate_resume(db_session, rating_data)
    updated_resume = db_session.query(Resume).filter(Resume.id == resume.id).first()
    assert updated_resume.rating == 4.0
    assert updated_resume.num_ratings == 1
