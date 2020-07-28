from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Statictics, Transaction, Wallet
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from paxful.settings import WALLET_TRANSFER_COMMISION_RATE


class UserSerializer(serializers.ModelSerializer):
    # token = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        fields = ["username", "email"]

    # def get_token(self, user):
    #     return Token.objects.get(user=user).key

    # def create(self, validated_data):
    #     """
    #     Create and return a new `User` instance, given the validated data.
    #     """
    #     # try:
    #     #     User.objects.get(username=self.initial_data['username']).exists()
    #     # except APIException as apiException:
    #     #     raise apiException

    #     email = self.initial_data["email"]
    #     password = self.initial_data["password"]
    #     username = self.initial_data["username"]
    #     return User.objects.create(username=username, email=email, password=password)


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "url": {"lookup_field": "address"}}

    def create(self, validated_data):
        """
        Create and return a new `Wallet` instance, given the validated data.
        """
        user = self.context["request"].user
        # Limit user to 10 wallets
        if Wallet.objects.filter(user=user).count() > 9:
            raise ValidationError
        return Wallet.objects.create(user=user, balance=Decimal("1.0"))


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    origin_wallet = WalletSerializer(many=True)
    destination_wallet = WalletSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ["origin_wallet", "destination_wallet", "code", "amount"]

    def create(self, validated_data):
        user = self.context["request"].user
        origin_wallet = self.validated_data["origin_wallet"]
        destination_wallet = self.validated_data["destination_wallet"]
        amount = self.validated_data["amount"]
        user_wallets = Wallet.objects.filter(user=user)
        if destination_wallet is not user_wallets:
            amount = amount * 100 / WALLET_TRANSFER_COMMISION_RATE
            return Transaction.objects.create(
                origin_wallet=origin_wallet, destination_wallet=destination_wallet, amount=amount
            )
        else:
            return Transaction.objects.create(
                origin_wallet=origin_wallet, destination_wallet=destination_wallet, amount=amount
            )


class StaticticsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Statictics
        fields = ["origin_wallet", "destination_wallet", "code", "amount"]
