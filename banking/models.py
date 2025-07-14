from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.username}"