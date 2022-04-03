import pytest
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_404_NOT_FOUND

from students.models import Course


@pytest.fixture
def specify_settings(settings):
    # Тестовые данные для одного курса
    settings.TEST_COURSE = {
        'id': 1,
        'name': 'Тестовый курс'
    }

    # Количество создаваемых тестовых данных для курсов
    settings.TEST_COURSES_QUANTITY = 100

    # api urls
    settings.URL_API = 'http://127.0.0.1:8000/api/v1'
    settings.URL_COURSES = '/courses/'
    settings.URL_API_COURSES = settings.URL_API + settings.URL_COURSES

    return settings


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_retrieve_course(client, course_factory, specify_settings):
    """
    Проверка получения одного курса (retrieve-логика).
    """

    courses = course_factory(_quantity=1)

    url = f'{specify_settings.URL_API_COURSES}{courses[0].id}/'
    response = client.get(url)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert data.get('id') == courses[0].id
    assert data.get('name') == courses[0].name

    # Проверка ответа на не существующий курс
    url = f'{specify_settings.URL_API_COURSES}999/'
    response = client.get(url)

    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_list_courses(client, course_factory, specify_settings):
    """
    Проверка получения списка курсов (list-логика).
    """

    courses = course_factory(_quantity=specify_settings.TEST_COURSES_QUANTITY)

    response = client.get(specify_settings.URL_API_COURSES)

    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_courses(client, course_factory, specify_settings):
    """
    Проверка фильтрации курсов по идентификатору и наименованию.
    """

    courses = course_factory(_quantity=specify_settings.TEST_COURSES_QUANTITY)

    response = client.get(specify_settings.URL_API_COURSES)

    assert response.status_code == HTTP_200_OK

    data = response.json()
    for value in data:
        #  Проверка фильтрации по id курса
        data = {'id': value['id']}
        response = client.get(specify_settings.URL_API_COURSES, data)

        assert response.status_code == HTTP_200_OK

        #  Проверка фильтрации по name курса
        data = {'name': value['name']}
        response = client.get(specify_settings.URL_API_COURSES, data)

        assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_create_course(client, specify_settings):
    """
    Проверка создания курса через api
    """
    count = Course.objects.count()

    response = client.post(specify_settings.URL_API_COURSES, data=specify_settings.TEST_COURSE)

    assert response.status_code == HTTP_201_CREATED
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory, specify_settings):
    """
    Проверка обновления названия курса через api
    """
    course = course_factory(_quantity=1)
    data = {
        'name': specify_settings.TEST_COURSE['name']
    }
    url = f'{specify_settings.URL_API_COURSES}{course[0].id}/'

    response = client.patch(url, data=data)
    response_get = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert response_get.json().get('name') == data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory, specify_settings):
    """
    Проверка удаления курса через api
    """
    course = course_factory(_quantity=1)
    count = Course.objects.count()

    url = f'{specify_settings.URL_API_COURSES}{course[0].id}/'
    response = client.delete(url)

    assert (response.status_code == HTTP_204_NO_CONTENT) or (response.status_code == HTTP_200_OK)
    assert Course.objects.count() == count - 1
