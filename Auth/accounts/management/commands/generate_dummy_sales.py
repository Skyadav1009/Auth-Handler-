from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, Inventory
import random
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generate dummy users and inventory data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating dummy data...")

        # Create/Get 3 test users
        users_data = [
            {'username': 'seller1', 'email': 'shivam.seller1@gmail.com', 'password': 'Password123!', 'role': 'employee', 'gender': 'Male', 'age': 25, 'salary': 45000.00},
            {'username': 'seller2', 'email': 'shivam.seller2@gmail.com', 'password': 'Password123!', 'role': 'employee', 'gender': 'Female', 'age': 30, 'salary': 55000.00},
            {'username': 'seller3', 'email': 'shivam.seller3@gmail.com', 'password': 'Password123!', 'role': 'employee', 'gender': 'Male', 'age': 28, 'salary': 48000.00},
        ]

        items = ["PC", "AC", "Fridge", "Microwave", "Smart TV", "Washing Machine", "Smartphone"]

        count = 0
        for u_data in users_data:
            user, created = User.objects.get_or_create(
                username=u_data['username'],
                email=u_data['email']
            )
            if created:
                user.set_password(u_data['password'])
                user.save()
            
            # Update or create profile safely to ensure no conflict with project's existing logic
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'role': u_data['role'],
                    'gender': u_data['gender'],
                    'age': u_data['age'],
                    'salary': u_data['salary'],
                }
            )

            # Insert 3 to 4 random inventory records for each user
            num_items = random.randint(3, 4)
            for _ in range(num_items):
                random_days_ago = random.randint(0, 30)
                Inventory.objects.create(
                    inventory_name=random.choice(items),
                    price=round(random.uniform(5000.00, 75000.00), 2),
                    date=timezone.now().date() - timedelta(days=random_days_ago),
                    user=user
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f"Successfully processed user {user.email}"))

        self.stdout.write(self.style.SUCCESS(f'Done! Successfully generated {count} inventory records.'))
