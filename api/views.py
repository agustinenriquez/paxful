from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, TransactionSerializer, WalletSerializer, StaticticsSerializer
from web.models import Transaction, Wallet
from .models import Statictics
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        return Response("")


class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Wallet.objects.all().order_by("-date_joined")
    serializer_class = WalletSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Transaction.objects.all().order_by("-date_joined")
    serializer_class = TransactionSerializer


class StaticticsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Statictics.objects.all().order_by("-date_joined")
    serializer_class = StaticticsSerializer
