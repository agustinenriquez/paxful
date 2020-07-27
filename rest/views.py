from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, TransactionSerializer, WalletSerializer
from web.models import Transaction
from .models import Statictics
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        username = self.request.data['username']
        password = self.request.data['password']
        email = self.request.data['email']
        obj = serializer.save()
        Token.objects.create(user=obj)
        return super().perform_create(serializer)


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
