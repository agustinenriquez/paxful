import django; django.setup()
import factory
import factory.fuzzy
from django.contrib.auth.models import User

from web import models


factory.Faker._DEFAULT_LOCALE = "en_US"


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
