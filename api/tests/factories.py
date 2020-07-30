import factory
from decimal import Decimal


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)

    username = "agustest"
    password = factory.PostGenerationMethodCall("set_password", "aguspass")
    email = "agustest@gmail.com"


class SuperUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)

    username = "adminagustest"
    password = factory.PostGenerationMethodCall("set_password", "aguspass")
    email = "adminagustest@gmail.com"

    is_superuser = True
    is_staff = True
    is_active = True


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "api.Wallet"
        django_get_or_create = ("address",)

    user = factory.SubFactory(UserFactory)
    balance = factory.Faker("pydecimal")
    alias = "testwallet"
    address = factory.Faker("uuid4")


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "api.Transaction"

    origin_address = factory.Faker("uuid4")
    destination_address = factory.Faker("uuid4")
    amount = Decimal("0.5")
    code = ""


class PlatformFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "api.Platform"

    name = "paxful"
    profit = Decimal("0")
