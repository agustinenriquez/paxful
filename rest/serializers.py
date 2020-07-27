from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Transaction
from web.models import Wallet

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['origin_wallet', 'destination_wallet', 'code', 'amount']


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallet
        fields = ['origin_wallet', 'destination_wallet', 'code', 'amount']


