import pytest

from mt_jwt_auth_apps.jwt_user.models import User
from ..views import jwt_token_handler
from rest_framework.test import APIClient
from django.contrib.auth.models import Group

pytestmark = pytest.mark.django_db


@pytest.fixture
def drf_api_client():
    return APIClient()


def add_user_to_groups(user, groups=tuple()):
    for group_name in groups:
        group = Group(name=group_name)
        group.save()
        group.user_set.add(user)
    return True


def create_user_get_token(username='test', email='sergei@decorist.com', groups=tuple()):
    user = User(username=username, email=email, password='!')
    user.set_password('xhkwyb12')
    user.save()
    add_user_to_groups(user, groups)
    token = jwt_token_handler(user, user.uuid)
    return user, token


def test_get_jwt(drf_api_client):
    response = drf_api_client.get('/api/v1/account/obtain-jwt/')
    assert response.status_code == 200, str(response.status_text)


def test_get_login(drf_api_client):
    response = drf_api_client.get('/api/v1/account/login/')
    assert response.status_code == 405, str(response.status_text)


def test_logout(drf_api_client):
    response = drf_api_client.get('/api/v1/account/logout/')
    assert response.status_code == 401, str(response.status_text)


def test_post_login(drf_api_client):
    user, token = create_user_get_token(username='root', email='sergei@decorist.com')
    response = drf_api_client.post('/api/v1/account/login/', {'username': 'root', 'password': 'xhkwyb12'})
    assert response.data == token, str(response.content)


def test_authentication_view_post(drf_api_client):
    user, token = create_user_get_token()
    drf_api_client.credentials(HTTP_AUTHORIZATION='JWT ' + token.decode("utf-8"))
    response = drf_api_client.post('/api/v1/account/test-authentication-view/', {'test': 'test'})
    assert response.data == {'post', 1}, str(response.content)


def test_authentication_view_get(drf_api_client):
    user, token = create_user_get_token()
    drf_api_client.credentials(HTTP_AUTHORIZATION='JWT ' + token.decode("utf-8"))
    response = drf_api_client.get('/api/v1/account/test-authentication-view/')
    assert response.data == {'get', 1}, str(response.content)


def test_permission_view_post(drf_api_client):
    user, token = create_user_get_token(groups=('ADMIN',))
    drf_api_client.credentials(HTTP_AUTHORIZATION='JWT ' + token.decode("utf-8"))
    response = drf_api_client.post('/api/v1/account/test-permission-view/', {'test': 'test'})
    assert response.data == {'post', 1}, str(response.content)


def test_permission_view_get(drf_api_client):
    user, token = create_user_get_token()
    drf_api_client.credentials(HTTP_AUTHORIZATION='JWT ' + token.decode("utf-8"))
    response = drf_api_client.get('/api/v1/account/test-permission-view/')
    assert response.data == {'get', 1}, str(response.content)
