from django.db import models
from django.contrib.auth.models import AbstractUser


# -----------------------------------------------------------
# LOGIN TABLE
# -----------------------------------------------------------
class Login(AbstractUser):
    userType = models.CharField(max_length=100)     # admin / user
    viewPass = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username


# -----------------------------------------------------------
# USER PROFILE TABLE
# -----------------------------------------------------------
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=300)
    image = models.ImageField(upload_to="user_images", null=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    status = models.CharField(max_length=40, default='pending', null=True)

    def __str__(self):
        return self.name


# -----------------------------------------------------------
# SHOP PROFILE TABLE
# -----------------------------------------------------------
class Shop(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=300)
    image = models.ImageField(upload_to="shop_images", null=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    # pending → approved → rejected → blocked
    status = models.CharField(max_length=40, default='pending', null=True)

    def __str__(self):
        return self.name


# -----------------------------------------------------------
# USER UPLOAD DRAWINGS
# -----------------------------------------------------------
class Drawing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300, null=True)
    image = models.ImageField(upload_to="drawings")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


# -----------------------------------------------------------
# VIDEOS UPLOADED BY ADMIN (YOUTUBE LINKS)
# -----------------------------------------------------------
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, null=True)
    category = models.CharField(max_length=100, default="General")
    video_link = models.CharField(max_length=500)     # YouTube link only
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=40, default="active")

    def __str__(self):
        return self.title


# -----------------------------------------------------------
# USER REQUEST TO WATCH VIDEO
# -----------------------------------------------------------
class VideoRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    # pending → approved → rejected
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.user.name} → {self.video.title}"


# -----------------------------------------------------------
# PRODUCTS ADDED BY ADMIN
# -----------------------------------------------------------
class Products(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)       # Normal text field
    price = models.IntegerField()
    qty = models.IntegerField()
    image = models.ImageField(upload_to="product_images")
    desc = models.CharField(max_length=300)
    status = models.CharField(max_length=100, default="Available")

    def __str__(self):
        return self.name


# -----------------------------------------------------------
# ORDER TABLE
# -----------------------------------------------------------
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(null=True)
    status = models.CharField(max_length=40, default='Pending', null=True)

    def __str__(self):
        return f"Order {self.id}"


# -----------------------------------------------------------
# CART TABLE
# -----------------------------------------------------------
class Cart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    qnty = models.IntegerField(null=True)
    amt = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=40, default='pending', null=True)

    def __str__(self):
        return f"{self.product.name} x {self.qnty}"





class DrawingFeedback(models.Model):
    drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.drawing.title} by {self.user.name}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    name_on_card = models.CharField(max_length=50)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.name}"


class ProductFeedback(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.product.name}"
