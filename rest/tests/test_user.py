import requests
import pytest
import uuid
from factories import UserFactory
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class DB:
    def __init__(self):
        self.intransaction = []

    def begin(self, name):
        self.intransaction.append(name)

    def rollback(self):
        self.intransaction.pop()


@pytest.fixture(scope="module")
def db():
    return DB()


@pytest.fixture
def test_password():
   return 'strong-test-pass'


@pytest.fixture
def create_user(db, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return User.objects.create_user(**kwargs)
   return make_user


@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()


@pytest.fixture
def get_or_create_token(db, create_user):
   user = create_user()
   token, _ = Token.objects.get_or_create(user=user)
   return token


def test_user_is_active():
    user = UserFactory.create()
    assert user.is_active is True


def test_create_user_using_post_request(api_client):
    user = UserFactory.create()
    r = api_client.post("http://127.0.0.1/users/", {'username': user.username, 'password': user.password, 'email': user.email})
    if r.status_code == 201:
        assert True
    else:
        assert False


def test_create_user_and_get_token(api_client, get_or_create_token):
    user = UserFactory.create()
    r = api_client.post("http://127.0.0.1/users/", {'username': user.username, 'password': user.password, 'email': user.email})
    token = get_or_create_token
    assert token is not None
