import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()
from django.contrib.auth.models import User
print("--- Current Users in Database ---")
for u in User.objects.all():
    print(f"ID: {u.id}, Username: '{u.username}', Email: '{u.email}'")
print("---------------------------------")
