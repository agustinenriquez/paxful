from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, TransactionSerializer, WalletSerializer
from web.models import Transaction
from .models import Statictics


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


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
    queryset = Transaction.objects.all().order_by('-date_joined')
    serializer_class = WalletSerializer


class StaticticsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Statictics.objects.all().order_by('-date_joined')
    serializer_class = WalletSerializer
