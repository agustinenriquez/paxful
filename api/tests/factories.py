import django

import factory
import factory.fuzzy
from django.contrib.auth.models import User
from web.models import Wallet

django.setup()


factory.Faker._DEFAULT_LOCALE = "en_US"


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class WalletFactory(factory.Factory):
    class Meta:
        model = Wallet

    user = UserFactory.create()
    balance = factory.Faker("balance")
    alias = factory.Faker("alias")
