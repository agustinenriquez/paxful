from django.db import models
import random
import string


class Wallet(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=False, blank=False)
    balance = models.DecimalField(decimal_places=8, default=0, max_digits=10)
    alias = models.CharField(max_length=50, default="mywallet")

    def __str__(self):
        return self.user.username


class Transfer(models.Model):
    origin_wallet = models.OneToOneField("Wallet", related_name="origin_wallet", on_delete=models.CASCADE)
    destination_wallet = models.OneToOneField("Wallet", related_name="destination_wallet", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=6, default=0, max_digits=10)
    code = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.code = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        super().save(*args, **kwargs)


class Transaction(models.Model):
    pass
