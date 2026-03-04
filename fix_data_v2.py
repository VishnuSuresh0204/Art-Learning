
import os
import django
import sys

# Add the project directory to sys.path
sys.path.append(r'c:\Users\admin\Documents\python pro\art_gallary\art_gallary\art')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'art.settings')
django.setup()

from myapp.models import User

print("--- Fixing User Names ---")
users = User.objects.filter(name="")
print(f"Found {users.count()} users with empty names.")

for user in users:
    username = user.loginid.username
    print(f"Updating user {user.id}: setting name to '{username}'")
    user.name = username
    user.save()

print("Data fix complete!")
