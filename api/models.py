from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random
import string
from decimal import Decimal
import uuid


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Statictics(models.Model):
    pass


class Wallet(models.Model):
    user = models.ForeignKey(
        "auth.User", related_name="wallet_user", on_delete=models.CASCADE, null=False, blank=False,
    )
    balance = models.DecimalField(decimal_places=25, default=Decimal("1.0"), max_digits=50)
    alias = models.CharField(max_length=50, default="mywallet")
    address = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.user.username


class Transfer(models.Model):
    origin_wallet = models.ForeignKey("Wallet", related_name="origin_wallet", on_delete=models.CASCADE)
    destination_wallet = models.ForeignKey("Wallet", related_name="destination_wallet", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=25, default=0, max_digits=50)
    code = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        self.code = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        super().save(*args, **kwargs)


class Transaction(models.Model):
    pass
