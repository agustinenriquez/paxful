import pytest
from rest_framework.test import APIClient
from .factories import WalletFactory, PlatformFactory
from decimal import Decimal


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_user(api_client):
    response = api_client.get("/users/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_with_credentials(api_client, django_user_model):
    username, password = "agustest", "agustestpass"
    django_user_model.objects.create_user(username=username, password=password)
    api_client.login(username=username, password=password)
    response = api_client.get("/users/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallet(api_client, django_user_model):
    username, password = "agustest", "agustestpass"
    django_user_model.objects.create_user(username=username, password=password)
    api_client.login(username=username, password=password)
    response = api_client.get("/wallets/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallet_without_credentials(api_client):
    response = api_client.get("/wallets/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_wallet_retrieve(api_client, django_user_model):
    username, password = "agustest", "agustestpass"
    wallet = WalletFactory.create(user=django_user_model.objects.create_user(username=username, password=password))
    api_client.login(username=username, password=password)
    response = api_client.get(f"/wallets/{wallet.address}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallet_retrieve_balance(api_client, django_user_model):
    username, password = "agustest", "agustestpass"
    wallet = WalletFactory.create(user=django_user_model.objects.create_user(username=username, password=password))
    api_client.login(username=username, password=password)
    response = api_client.get(f"/wallets/{wallet.address}/")
    assert response.status_code == 200
    assert Decimal(response.data["balance"]) == wallet.balance


@pytest.mark.django_db
def test_transaction_retrieve(api_client, django_user_model):
    username, password = "agustest", "agustestpass"
    WalletFactory.create(user=django_user_model.objects.create_user(username=username, password=password))
    api_client.login(username=username, password=password)
    response = api_client.get("/transactions/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_transaction_create(api_client, django_user_model):
    username, password = "agustest", "agustestpass"
    origin_user = django_user_model.objects.create_user(username=username, password=password)
    username, password = "agustest2", "agustestpass2"
    destination_user = django_user_model.objects.create_user(username=username, password=password)
    origin_wallet = WalletFactory.create(user=origin_user)
    destination_wallet = WalletFactory.create(user=destination_user)
    api_client.login(username=username, password=password)
    response = api_client.post(
        "/transactions/",
        {
            "origin_address": origin_wallet.address,
            "destination_address": destination_wallet.address,
            "amount": Decimal("0.02"),
        },
        type="json",
    )
    assert response.status_code == 201


def test_statictics_retrieve(admin_client):
    PlatformFactory.create()
    response = admin_client.get("/statistics/")
    assert response.status_code == 200
