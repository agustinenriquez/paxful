from factory import django
from api.models import Platform, Transaction
import factory
from decimal import Decimal
import uuid
import random
import string


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)

    username = "agustest"
    password = factory.PostGenerationMethodCall("set_password", "eduzen!")
    email = "agustest@gmail.com"


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "api.Wallet"
        django_get_or_create = ("address",)

    user = UserFactory.create()
    balance = Decimal("1.0")
    alias = "testwallet"
    address = uuid.uuid4()


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "api.Transaction"
        django_get_or_create = ("code",)

    origin_address = WalletFactory.create().address
    destination_address = WalletFactory.create().address
    amount = Decimal("0.5")
    code = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


class PlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "api.Platform"
        django_get_or_create = ("name",)

    name = "paxful"
    profit = Decimal("0")
