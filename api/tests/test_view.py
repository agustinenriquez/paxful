import pytest
from rest_framework.test import APIClient
from .factories import WalletFactory, UserFactory, SuperUserFactory
from decimal import Decimal


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_user(api_client):
    response = api_client.get("/users/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_with_credentials(api_client):
    user = UserFactory.create()
    api_client.force_authenticate(user=user)
    response = api_client.get("/users/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallet(api_client):
    user = UserFactory.create()
    api_client.force_authenticate(user=user)
    response = api_client.get("/wallets/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallet_without_credentials(api_client):
    response = api_client.get("/wallets/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_wallet_retrieve(api_client):
    user = UserFactory.create()
    wallet = WalletFactory.create(user=user)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/wallets/{wallet.address}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_wallet_retrieve_balance(api_client):
    user = UserFactory.create()
    wallet = WalletFactory.create(user=user)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/wallets/{wallet.address}/")
    assert response.status_code == 200
    assert Decimal(response.data["balance"]) == wallet.balance


@pytest.mark.django_db
def test_transaction_retrieve(api_client):
    user = UserFactory.create()
    api_client.force_authenticate(user=user)
    response = api_client.get("/transactions/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_transaction_create(api_client):
    user = UserFactory.create()
    origin_wallet = WalletFactory.create(user=user)
    destination_wallet = WalletFactory.create(user=UserFactory.create())
    api_client.force_authenticate(user=user)
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


@pytest.mark.django_db
def test_statictics_retrieve_with_admin(api_client):
    user = SuperUserFactory.create()
    api_client.force_authenticate(user=user)
    response = api_client.get("/statictics/")
    assert response.status_code == 200
