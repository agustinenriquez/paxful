from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, TransactionSerializer, WalletSerializer
from .models import Transaction, Wallet, Platform
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().filter(id=self.request.user.pk)
        return queryset


class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wallets to be viewed or created by registered users.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "address"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed or created by registered users.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(origin_address__in=Wallet.objects.filter(user=self.request.user).values_list("address", flat=True))
        )
        return queryset


class StaticticsViewSet(viewsets.ViewSet):
    """
    API endpoint that allows statictics to be viewed by admins.
    """

    permission_classes = (IsAdminUser,)

    def list(self, request, format=None):
        paxful_profit = Platform.objects.first().profit
        total_transactions = Transaction.objects.all().count()

        return Response({"transactions": total_transactions, "profit": paxful_profit})
