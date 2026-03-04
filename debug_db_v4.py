
import os
import django
import sys

# Add the project directory to sys.path
sys.path.append(r'c:\Users\admin\Documents\python pro\art_gallary\art_gallary\art')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'art.settings')
django.setup()

from myapp.models import ProductFeedback, Order, Products, User

print("--- Checking Product Feedback & Images ---")
feedbacks = ProductFeedback.objects.all()
for f in feedbacks:
    print(f"ID: {f.id}")
    print(f"Product: {f.product.name}")
    try:
        if f.product.image:
            print(f"Image URL: {f.product.image.url}")
        else:
            print("Image field is empty/None")
    except Exception as e:
        print(f"Error accessing image URL: {e}")
    
    print(f"User: {f.user.name} ({f.user.email})")
    print("-" * 20)
