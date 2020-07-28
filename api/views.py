from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, TransactionSerializer, WalletSerializer, StaticticsSerializer
from .models import Transaction, Wallet, Statictics


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
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "address"

    def get_queryset(self):
        queryset = super().get_queryset().filter(id=self.request.user.pk)
        return queryset


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
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


class StaticticsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Statictics.objects.all().order_by("-date_joined")
    serializer_class = StaticticsSerializer
    permission_classes = (IsAuthenticated,)
