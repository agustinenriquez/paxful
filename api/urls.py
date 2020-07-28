from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from api.views import UserViewSet, WalletViewSet, TransactionViewSet, StaticticsViewSet, HelloView

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"wallets", WalletViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"statistics", StaticticsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", views.obtain_auth_token),
    path("hello/", HelloView.as_view(), name="hello"),
]
