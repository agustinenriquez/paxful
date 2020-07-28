from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Statictics, Transaction, Wallet
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from paxful.settings import WALLET_TRANSFER_COMMISION_RATE
from .helpers import get_current_BTC_to_USD_price


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
    balance_in_usd = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Wallet
        fields = ["balance", "balance_in_usd"]
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

    def get_balance_in_usd(self, obj):
        return get_current_BTC_to_USD_price()


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ["origin_address", "destination_address", "code", "amount"]

    def create(self, validated_data):
        user = self.context["request"].user
        origin_address = self.validated_data["origin_address"]
        destination_address = self.validated_data["destination_address"]
        amount = self.validated_data["amount"]
        user_wallets_addresses = Wallet.objects.filter(user=user).values_list("address", flat=True)
        destination_wallet = Wallet.objects.get(address=destination_address)
        origin_wallet = Wallet.objects.get(address=origin_address)

        if origin_wallet.amount < amount:
            # Doesnt have enough funds.
            raise ValidationError

        if destination_address in user_wallets_addresses:
            destination_wallet.balance += amount
            destination_wallet.save()
            origin_wallet.balance -= amount
            origin_wallet.save()

            return Transaction.objects.create(
                origin_address=origin_address, destination_address=destination_address, amount=amount
            )
        else:
            fee = amount * WALLET_TRANSFER_COMMISION_RATE
            amount = amount - fee
            destination_wallet.balance += amount
            destination_wallet.save()
            origin_wallet.balance -= amount
            origin_wallet.save()

            return Transaction.objects.create(
                origin_address=origin_address, destination_address=destination_address, amount=amount
            )


class StaticticsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Statictics
        fields = ["origin_wallet", "destination_wallet", "code", "amount"]
