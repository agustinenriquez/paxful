from django.urls import path
from web.views import UserCreateView, WalletCreateView, TransferCreateView, WalletListView, post_users

urlpatterns = [
    path("", UserCreateView.as_view(), name="index"),
    path("wallet/add/", WalletCreateView.as_view(), name="create-wallet"),
    path("wallet/all", WalletListView.as_view(), name="list-wallet"),
    path("wallet/<int:pk>/transfer/", TransferCreateView.as_view(), name="wallet-transfer"),
]
