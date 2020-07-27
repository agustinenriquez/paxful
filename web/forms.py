from django.contrib.auth.models import User
from django import forms
from .models import Wallet, Transfer


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password", "email")


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ("alias", "balance")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = User.objects.filter(id=self.request.user.id)
        self.fields.initial["items"].queryset = user


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ("origin_wallet", "destination_wallet", "amount")
