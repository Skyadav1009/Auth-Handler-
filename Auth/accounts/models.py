from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('employee', 'Employee'),
        ('seller', 'Seller'),
    ]
    USER_TYPE_CHOICES = (
        ("seller", "Seller"),
        ("customer", "Customer"),
        ("staff", "Staff"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # New fields added safely as nullable to not break existing data
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Inventory(models.Model):
    inventory_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventories')

    def __str__(self):
        return f"{self.inventory_name} - {self.user.username}"

