from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Statictics, Transaction, Wallet
from rest_framework.exceptions import APIException


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        fields = ["token"]

    def get_token(self, user):
        return Token.objects.get(user=user).key

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        # try:
        #     User.objects.get(username=self.initial_data['username']).exists()
        # except APIException as apiException:
        #     raise apiException

        email = self.initial_data["email"]
        password = self.initial_data["password"]
        username = self.initial_data["username"]
        return User.objects.create(username=username, email=email, password=password)


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ["origin_wallet", "destination_wallet", "code", "amount"]


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallet
        fields = ["origin_wallet", "destination_wallet", "code", "amount"]

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        username = self.initial_data["username"]
        if Wallet.objects.filter(user_username=username).count() < 9:
            return Wallet.objects.create(username=username)
        else:
            raise APIException


class StaticticsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Statictics
        fields = ["origin_wallet", "destination_wallet", "code", "amount"]
