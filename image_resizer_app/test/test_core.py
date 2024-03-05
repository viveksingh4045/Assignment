# tests.py

import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User

from core.views import index

@pytest.fixture
def rf():
    return RequestFactory()


def test_my_view(rf, user, my_model):
    request = rf.get('/')
    response = index(request)
    assert response.status_code == 200
