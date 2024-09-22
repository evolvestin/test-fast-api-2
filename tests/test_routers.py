

def creation_of_test_resume(client):
    """Запрос на создание тестового резюме"""
    response = client.post(
        '/upload/',
        data={'candidate_name': 'Test Testerov Testerovich'},
        files={'file': ('resume.pdf', b'PDF content', 'application/pdf')}
    )
    return response


def test_create_resume(client):
    """Тест на создание резюме"""
    response = creation_of_test_resume(client)
    assert response.status_code == 200
    data = response.json()
    assert data['candidate_name'] == 'Test Testerov Testerovich'
    assert 'id' in data


def test_list_resumes(client):
    """Тест на получение списка резюме"""
    creation_of_test_resume(client)  # Сначала создаем резюме, чтобы был список

    response = client.get('/list/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_delete_resume(client):
    """Тест на удаление резюме"""

    response = creation_of_test_resume(client)  # Сначала создаем резюме, чтобы получить его ID
    resume_id = response.json()['id']

    # Затем удаляем созданное резюме
    delete_response = client.delete(f'/delete/{resume_id}')
    assert delete_response.status_code == 200
    assert delete_response.json() == {'msg': 'Resume deleted successfully'}

    # Проверяем, что резюме действительно удалено
    response = client.get('/list/')
    data = response.json()
    assert not any(resume['id'] == resume_id for resume in data)


def test_rate_resume(client):
    """Тест на оценку резюме"""
    resume_id = creation_of_test_resume(client).json()['id']  # Сначала создаем резюме, чтобы получить его ID

    # Оцениваем созданное резюме
    rating_response = client.post(
        '/rate/',
        json={'resume_id': resume_id, 'user_rating': 4.5}
    )
    assert rating_response.status_code == 200
    data = rating_response.json()
    assert data['resume_id'] == resume_id
    assert data['user_rating'] == 4.5

    # Проверяем, что рейтинг резюме обновлен
    response = client.get('/list/')
    resume = next(resume for resume in response.json() if resume['id'] == resume_id)
    assert resume['rating'] == 4.5
    assert resume['num_ratings'] == 1
