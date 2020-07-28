from django.urls import include, path
from rest_framework_nested import routers
from api.views import UserViewSet, WalletViewSet, TransactionViewSet, StaticticsViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"wallets", WalletViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"statistics", StaticticsViewSet, basename="statistics")

wallet_router = routers.NestedSimpleRouter(router, r"wallets", lookup="wallets")
wallet_router.register(r"transactions", TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(wallet_router.urls)),
]
