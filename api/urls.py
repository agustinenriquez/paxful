from django.urls import include, path
from rest_framework import routers
from api.views import UserViewSet, WalletViewSet, TransactionViewSet, StaticticsViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"wallets", WalletViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"statistics", StaticticsViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
