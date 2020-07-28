from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random
import string
from decimal import Decimal
import uuid
from helpers import get_current_BTC_to_USD_price


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Wallet(models.Model):
    user = models.ForeignKey(
        "auth.User", related_name="wallet_user", on_delete=models.CASCADE, null=False, blank=False,
    )
    balance = models.DecimalField(decimal_places=25, default=Decimal("1.0"), max_digits=50)
    alias = models.CharField(max_length=50, default="mywallet")
    address = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    origin_address = models.UUIDField(default=None)
    destination_address = models.UUIDField(default=None)
    amount = models.DecimalField(decimal_places=25, default=0, max_digits=50)
    code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        super().save(*args, **kwargs)


class Platform(models.Model):
    name = models.CharField(max_length=50, blank=True, verbose_name="Paxful")
    profit = models.DecimalField(decimal_places=25, default=0, max_digits=50)
    profit_to_USD = models.DecimalField(decimal_places=10, default=0, max_digits=10)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        current_btc_to_dollar_price = get_current_BTC_to_USD_price()
        self.profit_to_USD = self.profit * current_btc_to_dollar_price
        super().save(*args, **kwargs)


class Statictics(models.Model):
    platform = models.OneToOneField("Platform", on_delete=models.CASCADE, null=False, blank=False)
    transactions = models.ForeignKey("Transactions", on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.platform
