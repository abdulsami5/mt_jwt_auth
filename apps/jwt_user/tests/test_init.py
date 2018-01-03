import pytest

from rest_framework.test import APIRequestFactory
#
# # Using the standard RequestFactory API to create a form POST request
# factory = APIRequestFactory()
# request = factory.get('/api/v1/account/obtain-jwt/', {'title': 'new idea'})
from apps.jwt_user.models import User
from ..views import ObtainJSONWebToken, jwt_token_handler
from django.test import Client
from rest_framework.test import APIClient

client = APIClient()
factory = APIRequestFactory()
pytestmark = pytest.mark.django_db


def test_get_jwt(client):
    response = client.get('/api/v1/account/obtain-jwt/')
    assert response.status_code == 200, str(response.status_text)


def test_get_login(client):
    response = client.get('/api/v1/account/login/')
    assert response.status_code == 405, str(response.status_text)


def test_logout(client):
    response = client.get('/api/v1/account/logout/')
    assert response.status_code == 401, str(response.status_text)


def create_user(username='xxx', email='sergei@decorist.com'):
    user = User(username=username, email='sergei@decorist.com', password='!')
    user.set_password('xhkwyb12')
    user.save()
    return user


def test_post_login():
    user = create_user(username='root', email='sergei@decorist.com')
    token = jwt_token_handler(user, user.uuid)
    response = client.post('/api/v1/account/login/', {'username': 'root', 'password': 'xhkwyb12'})
    assert response.data == token, str(response.content)
