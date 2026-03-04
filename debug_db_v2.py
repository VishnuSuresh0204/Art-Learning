
import os
import django
import sys

# Add the project directory to sys.path
sys.path.append(r'c:\Users\admin\Documents\python pro\art_gallary\art_gallary\art')

# Assuming 'art' is the project name or it's 'art_gallary' depending on where settings.py is.
# Let's try 'art.settings' first if manage.py is in 'art' folder.
# Or if settings is in `art/art/settings.py` then it is `art.settings`.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'art.settings')
django.setup()

from myapp.models import ProductFeedback, Order, Products, User

print("--- Checking Product Feedback ---")
feedbacks = ProductFeedback.objects.all()
print(f"Total Product Feedbacks: {feedbacks.count()}")
for fb in feedbacks:
    print(f" - ID: {fb.id}, Product: {fb.product.name}, User: {fb.user.name}, Rating: {fb.rating}, Comment: {fb.comment}")

print("\n--- Checking Orders with Status 'Delivered' ---")
delivered_orders = Order.objects.filter(status="Delivered")
print(f"Total Delivered Orders: {delivered_orders.count()}")
for order in delivered_orders:
    print(f" - ID: {order.id}, Customer: {order.customer.name}, Status: {order.status}")

print("\n--- Checking Products ---")
products = Products.objects.all()
print(f"Total Products: {products.count()}")
for p in products:
    print(f" - ID: {p.id}, Name: {p.name}")
