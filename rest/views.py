from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
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


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transaction.objects.all().order_by('-date_joined')
    serializer_class = TransactionSerializer


class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Wallet.objects.all().order_by('-date_joined')
    serializer_class = WalletSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class StaticticsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Statictics.objects.all().order_by('-date_joined')
    serializer_class = StaticticsSerializer
