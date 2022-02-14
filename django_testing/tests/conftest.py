import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker


# Фикстура апиклиента
@pytest.fixture
def client():
    return APIClient()


# Фабрика студентов
@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make("Student", **kwargs)

    return factory


# Фабрика курсов
@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make("Course", **kwargs)

    return factory
