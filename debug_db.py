
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'art_gallary.settings')
django.setup()

from art.myapp.models import ProductFeedback, Order, Products, User

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
