from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = (
        ("seller", "Seller"),
        ("customer", "Customer"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    gender = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


class Inventory(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'seller'})
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name