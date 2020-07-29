import pytest
from rest_framework.test import APIClient
from .factories import WalletFactory, UserFactory
from decimal import Decimal


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_user(api_client):
    response = api_client.get("/users/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallet(api_client):
    user = UserFactory.create()
    api_client.force_authenticate(user=user)
    response = api_client.get("/wallets/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallet_retrieve(api_client):
    user = UserFactory.create()
    wallet = WalletFactory.create(user=user)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/wallets/{wallet.address}/")
    assert response.status_code == 200
    assert Decimal(response.data["balance"]) == wallet.balance
