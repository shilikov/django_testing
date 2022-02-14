import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    ["course_id", "status_code"],
    (
        (1, HTTP_200_OK),
        (3, HTTP_404_NOT_FOUND)
    )
)
@pytest.mark.django_db
def test_courses_retrieve(course_id, status_code, client, course_factory, student_factory):
    course = course_factory(id=course_id)
    students = student_factory(_quantity=5)
    course.students.set(students)

    url = reverse('courses-detail', args=[1])
    response = client.get(url)

    assert response.status_code == status_code
    if response.status_code == HTTP_200_OK:
        assert len(response.data["students"]) == 5


@pytest.mark.parametrize(
    ["courses_qnt", "students_qnt"],
    (
        (4, 4),
        (5, 8)
    )
)
@pytest.mark.django_db
def test_courses_list(courses_qnt, students_qnt, client, course_factory, student_factory):
    courses = course_factory(_quantity=courses_qnt)
    for course in courses:
        students = student_factory(_quantity=students_qnt)
        course.students.set(students)

    url = reverse("courses-list")
    response = client.get(url)

    assert response.status_code != HTTP_404_NOT_FOUND
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == len(courses)


@pytest.mark.django_db
def test_courses_filter_id(client, course_factory, student_factory):
    courses = course_factory(_quantity=5)
    url = '{url}?{filter}={value}'.format(url=reverse("courses-list"), filter='id', value=courses[2].id)
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    if response.status_code == HTTP_200_OK:
        assert response.data[0]["id"] == courses[2].id


@pytest.mark.django_db
def test_courses_filter_name(client, course_factory, student_factory):
    courses = course_factory(_quantity=16)
    for course in courses:
        students = student_factory(_quantity=6)
        course.students.set(students)

    url = '{url}?{filter}={value}'.format(url=reverse("courses-list"), filter='name', value=courses[2].name)
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert response.data[0]["name"] == courses[2].name


@pytest.mark.django_db
def test_courses_create(client):
    data = {"id": 1, "name": "GYM"}
    url = reverse("courses-list")
    response = client.post(url, data=data)

    assert response.status_code == HTTP_201_CREATED
    if response.status_code == HTTP_201_CREATED:
        assert response.data["name"] == "GYM"

@pytest.mark.django_db
def test_courses_update(client, course_factory):
    courses = course_factory(_quantity=5)
    update_data = {
        "name": "Updatable"
    }

    url = reverse("courses-detail", args=[3])
    response = client.patch(url, update_data)

    assert response.status_code == HTTP_200_OK
    assert response.data["name"] == update_data["name"]


@pytest.mark.django_db
def test_courses_delete(client, course_factory):
    courses = course_factory(_quantity=5)

    url = reverse("courses-detail", args=[3])
    response = client.delete(url)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert response.data == None
