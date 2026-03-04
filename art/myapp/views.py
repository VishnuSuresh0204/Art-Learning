from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *



# ==============================================================================
#                               AUTHENTICATION VIEWS
# ==============================================================================

def home(request):
    """Landing page."""
    return render(request, 'index.html')

def about(request):
    """About page."""
    return render(request, 'about.html')

def register(request):
    """User registration view."""
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES.get('image')

        login_obj = Login.objects.create_user(
            username=username,
            password=password,
            userType="user",
            viewPass=password
        )

        user_obj = User(
            name=username,  # Saving username as default name
            email=email,
            phone=phone,
            address=address,
            image=image,
            loginid=login_obj
        )
        user_obj.save()

        messages.success(request, "Registration Successful!")
        return redirect("/login")

    return render(request, "register.html")


def shop_register(request):
    """Shop registration view."""
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES.get('image')

        # Create login object for shop - initially inactive
        login_obj = Login.objects.create_user(
            username=username,
            password=password,
            userType="shop",
            viewPass=password
        )
        login_obj.is_active = False # Admin must approve
        login_obj.save()

        shop_obj = Shop(
            name=username,
            email=email,
            phone=phone,
            address=address,
            image=image,
            loginid=login_obj,
            status="pending"
        )
        shop_obj.save()

        messages.success(request, "Registration Successful! Waiting for admin approval.")
        return redirect("/login")

    return render(request, "register_shop.html")


def login_view(request):
    """Login view handling User, Shop, and Admin logins."""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                messages.error(request, "Your account is not active. Please wait for admin approval.")
                return redirect("/login")
                
            # Check user type
            if user.userType == "admin":
                login(request, user)
                return redirect("/admin_home")
            elif user.userType == "shop":
                request.session['sid'] = user.id
                login(request, user)
                return redirect("/shop_home")
            else:
                # Custom session for regular users
                request.session['uid'] = user.id
                login(request, user)
                return redirect("/user_home")

        messages.error(request, "Invalid login credentials or account inactive")
        return redirect("/login")

    return render(request, "login.html")


# ==============================================================================
#                               USER VIEWS
# ==============================================================================

def user_home(request):
    """User Dashboard/Home"""
    if 'uid' not in request.session:
        return redirect("/login")

    user_login = Login.objects.get(id=request.session['uid'])
    profile = User.objects.get(loginid=user_login)

    return render(request, "USER/index.html", {"user": profile})


def shop_home(request):
    """Shop Dashboard/Home"""
    if 'sid' not in request.session:
        return redirect("/login")

    user_login = Login.objects.get(id=request.session['sid'])
    shop = Shop.objects.get(loginid=user_login)

    return render(request, "SHOP/index.html", {"shop": shop})


def shop_add_product(request):
    """Shop add its own product"""
    if 'sid' not in request.session:
        return redirect("/login")

    user_login = Login.objects.get(id=request.session['sid'])
    shop = Shop.objects.get(loginid=user_login)

    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        price = request.POST.get("price")
        qty = request.POST.get("qty")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")

        Products.objects.create(
            shop=shop,
            name=name,
            category=category,
            price=price,
            qty=qty,
            desc=desc,
            image=image
        )
        messages.success(request, "Product added successfully!")
        return redirect("/shop_view_products")

    return render(request, "SHOP/add_product.html")


def shop_view_products(request):
    """Shop view its own products"""
    if 'sid' not in request.session:
        return redirect("/login")

    user_login = Login.objects.get(id=request.session['sid'])
    shop = Shop.objects.get(loginid=user_login)
    products = Products.objects.filter(shop=shop)
    
    return render(request, "SHOP/view_products.html", {"products": products})


def shop_edit_product(request):
    """Shop edit its own product"""
    if 'sid' not in request.session:
        return redirect("/login")

    pid = request.GET.get("id")
    product = get_object_or_404(Products, id=pid)
    
    # Security check
    user_login = Login.objects.get(id=request.session['sid'])
    shop = Shop.objects.get(loginid=user_login)
    if product.shop != shop:
        return redirect("/shop_view_products")

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.category = request.POST.get("category")
        product.price = request.POST.get("price")
        product.qty = request.POST.get("qty")
        product.desc = request.POST.get("desc")
        product.status = request.POST.get("status")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()
        messages.success(request, "Product updated!")
        return redirect("/shop_view_products")

    return render(request, "SHOP/edit_product.html", {"product": product})


def shop_delete_product(request):
    """Shop delete its own product"""
    if 'sid' not in request.session:
        return redirect("/login")

    pid = request.GET.get("id")
    product = get_object_or_404(Products, id=pid)
    
    # Security check
    user_login = Login.objects.get(id=request.session['sid'])
    shop = Shop.objects.get(loginid=user_login)
    if product.shop == shop:
        product.delete()
        messages.success(request, "Product deleted.")
        
    return redirect("/shop_view_products")


def shop_view_bookings(request):
    """Shop view bookings for its products"""
    if 'sid' not in request.session:
        return redirect("/login")

    user_login = Login.objects.get(id=request.session['sid'])
    shop = Shop.objects.get(loginid=user_login)
    
    # Cart items for this shop's products where the order is paid or beyond
    cart_items = Cart.objects.filter(product__shop=shop).exclude(order__status="Pending").order_by('-date')
    
    return render(request, "SHOP/view_bookings.html", {"cart_items": cart_items})


def shop_update_booking_status(request):
    """Shop updates status of a specific booking item"""
    if 'sid' not in request.session:
        return redirect("/login")

    if request.method == "POST":
        cart_id = request.POST.get("cid")
        new_status = request.POST.get("status")
        cart_item = get_object_or_404(Cart, id=cart_id)
        
        # Security check
        user_login = Login.objects.get(id=request.session['sid'])
        shop = Shop.objects.get(loginid=user_login)
        if cart_item.product.shop == shop:
            cart_item.status = new_status
            cart_item.save()
            messages.success(request, f"Booking status updated to {new_status}")
            
    return redirect("/shop_view_bookings")


def profile(request):
    """View User Profile"""
    if 'uid' not in request.session:
        return redirect("/login")

    user_login = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=user_login)

    return render(request, "USER/profile.html", {"user": user})


def edit_profile(request):
    """Edit User Profile"""
    if 'uid' not in request.session:
        return redirect("/login")

    user_login = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=user_login)

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.address = request.POST.get("address")

        if request.FILES.get("image"):
            user.image = request.FILES.get("image")

        user.save()
        messages.success(request, "Profile Updated Successfully!")
        return redirect("/profile")

    return render(request, "USER/edit_profile.html", {"user": user})


def upload_drawing(request):
    """Upload a new drawing"""
    if 'uid' not in request.session:
        return redirect("login")

    user_login = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=user_login)

    if request.method == "POST":
        title = request.POST['title']
        desc = request.POST['description']
        img = request.FILES.get('image')

        Drawing.objects.create(
            user=user,
            title=title,
            description=desc,
            image=img
        )

        messages.success(request, "Drawing Uploaded!")
        return redirect("/view_drawings")

    return render(request, "USER/upload_drawing.html")


def all_drawings(request):
    """View all users' drawings (Gallery)"""
    if 'uid' not in request.session:
        return redirect("/login")
    drawings = Drawing.objects.all().order_by('-date')
    return render(request, "USER/view_drawings.html", {"drawings": drawings})


def my_drawings(request):
    """View current user's uploaded drawings"""
    if 'uid' not in request.session:
        return redirect("login")

    try:
        user_login = Login.objects.get(id=request.session['uid'])
        user = User.objects.get(loginid=user_login)
    except (Login.DoesNotExist, User.DoesNotExist):
        return redirect("login")

    drawings = Drawing.objects.filter(user=user)

    return render(request, "USER/my_drawing.html", {"drawings": drawings})


def drawing_detail(request):
    """View drawing details and feedback"""
    if 'uid' not in request.session:
        return redirect("/login")

    drawing_id = request.GET.get('id')
    drawing = get_object_or_404(Drawing, id=drawing_id)
    feedbacks = DrawingFeedback.objects.filter(drawing=drawing).order_by('-date')
    
    user_login = Login.objects.get(id=request.session['uid'])
    current_user = User.objects.get(loginid=user_login)

    if request.method == "POST":
        comment = request.POST.get('comment')
        if comment:
            DrawingFeedback.objects.create(
                drawing=drawing,
                user=current_user,
                comment=comment
            )
            messages.success(request, "Feedback added!")
            return redirect(f"/drawing_detail?id={drawing_id}")

    return render(request, "USER/drawing_detail.html", {
        "drawing": drawing,
        "feedbacks": feedbacks,
        "current_user": current_user
    })


def edit_feedback(request):
    """Edit own feedback"""
    if 'uid' not in request.session:
        return redirect("/login")

    feedback_id = request.GET.get("id")
    feedback = get_object_or_404(DrawingFeedback, id=feedback_id)
    
    # Ensure only the author can edit
    if feedback.user.loginid.id != request.session['uid']:
        messages.error(request, "You cannot edit this feedback.")
        return redirect(f"/drawing_detail?id={feedback.drawing.id}")

    if request.method == "POST":
        new_comment = request.POST.get("comment")
        if new_comment:
            feedback.comment = new_comment
            feedback.save()
            messages.success(request, "Feedback updated!")
            return redirect(f"/drawing_detail?id={feedback.drawing.id}")

    return render(request, "USER/edit_feedback.html", {"feedback": feedback})


def delete_drawing_feedback_user(request):
    """User delete own drawing feedback"""
    if 'uid' not in request.session:
        return redirect("/login")

    fid = request.GET.get("id")
    feedback = get_object_or_404(DrawingFeedback, id=fid)

    # Ensure only the author can delete
    if feedback.user.loginid.id != request.session['uid']:
        messages.error(request, "You cannot delete this feedback.")
        return redirect(f"/drawing_detail?id={feedback.drawing.id}")

    drawing_id = feedback.drawing.id
    feedback.delete()
    messages.success(request, "Feedback deleted!")
    return redirect(f"/drawing_detail?id={drawing_id}")


def delete_drawing(request):
    """Delete a drawing uploaded by the current user"""
    if 'uid' not in request.session:
        return redirect("/login")
    
    drawing_id = request.GET.get("id")
    if drawing_id:
        drawing = Drawing.objects.get(id=drawing_id)
        # Verify ownership
        if drawing.user.loginid.id == request.session['uid']:
             drawing.delete()
             
    return redirect(request.META.get('HTTP_REFERER', '/view_users'))


def user_view_videos(request):
    """User view tutorial videos"""
    videos = Video.objects.filter(status="active").order_by('-date')
    return render(request, "USER/view_videos.html", {"videos": videos})


def user_view_products(request):
    """User view shop products"""
    if 'uid' not in request.session:
        return redirect("/login")

    login_user = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=login_user)

    products = Products.objects.filter(status="Available")

    # Find all products already added to cart
    order = Order.objects.filter(customer=user, status="Pending").first()

    cart_product_ids = []
    if order:
        cart_product_ids = Cart.objects.filter(order=order).values_list("product_id", flat=True)

    return render(request, "USER/view_products.html", {
        "products": products, 
        "cart_product_ids": list(cart_product_ids)
    })


def add_to_cart(request):
    """Add item to cart"""
    if 'uid' not in request.session:
        messages.error(request, "Login required")
        return redirect("/login")

    login_user = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=login_user)

    product_id = request.GET.get("id")
    product = Products.objects.get(id=product_id)

    # Check/Create pending order
    order, created = Order.objects.get_or_create(
        customer=user,
        status="Pending",
        defaults={"amount": 0}
    )

    # Check if product already exists in cart
    existing_cart = Cart.objects.filter(order=order, product=product).first()

    if existing_cart:
        existing_cart.qnty += 1
        existing_cart.amt = existing_cart.qnty * product.price
        existing_cart.save()
    else:
        Cart.objects.create(
            order=order,
            product=product,
            qnty=1,
            amt=product.price
        )

    # Update total amount
    total = sum(item.amt for item in Cart.objects.filter(order=order))
    order.amount = total
    order.save()

    messages.success(request, "Product added to cart!")
    return redirect("/user_view_products")


def view_cart(request):
    """View User Cart"""
    if 'uid' not in request.session:
        messages.error(request, "Please login first")
        return redirect("/login")

    login_user = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=login_user)

    order = Order.objects.filter(customer=user, status="Pending").first()

    if not order:
        return render(request, "USER/cart.html", {"cart_items": None, "order": None})

    cart_items = Cart.objects.filter(order=order)
    total = sum(item.amt for item in cart_items)

    return render(request, "USER/cart.html", {
        "cart_items": cart_items,
        "order": order,
        "total": total
    })


def remove_cart(request):
    """Remove item from cart"""
    if 'uid' not in request.session:
        return redirect("/login")

    cart_id = request.GET.get("id")

    try:
        cart_item = Cart.objects.get(id=cart_id)
        order = cart_item.order
        cart_item.delete()

        # Update order total
        total = sum(item.amt for item in Cart.objects.filter(order=order))
        order.amount = total
        order.save()

    except Cart.DoesNotExist:
        pass

    return redirect("/view_cart")


def update_cart_quantity(request):
    """Update quantity of item in cart"""
    if 'uid' not in request.session:
        return redirect("/login")

    cart_id = request.GET.get("id")
    action = request.GET.get("action")  # "increase" or "decrease"

    try:
        cart_item = Cart.objects.get(id=cart_id)
        product = cart_item.product
        order = cart_item.order

        # Update quantity based on action
        if action == "increase":
            # Check if product has enough stock
            if product.qty > cart_item.qnty:
                cart_item.qnty += 1
            else:
                messages.warning(request, f"Only {product.qty} units available in stock!")
                return redirect("/view_cart")
        elif action == "decrease":
            if cart_item.qnty > 1:
                cart_item.qnty -= 1
            else:
                # If quantity becomes 0, remove the item
                cart_item.delete()
                # Update order total
                total = sum(item.amt for item in Cart.objects.filter(order=order))
                order.amount = total
                order.save()
                messages.info(request, "Item removed from cart")
                return redirect("/view_cart")

        # Update item amount
        cart_item.amt = cart_item.qnty * product.price
        cart_item.save()

        # Update order total
        total = sum(item.amt for item in Cart.objects.filter(order=order))
        order.amount = total
        order.save()

    except Cart.DoesNotExist:
        messages.error(request, "Cart item not found")

    return redirect("/view_cart")


def checkout(request):
    """Display checkout summary"""
    if 'uid' not in request.session:
        return redirect("/login")

    login_user = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=login_user)

    order = Order.objects.filter(customer=user, status="Pending").first()

    if not order:
        return redirect("/view_cart")

    cart_items = Cart.objects.filter(order=order)
    total = sum(item.amt for item in cart_items)

    return render(request, "USER/checkout.html", {
        "order": order,
        "total": total
    })


def process_payment(request):
    """Handle payment submission"""
    if 'uid' not in request.session:
        return redirect("/login")

    login_user = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=login_user)

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        account_number = request.POST.get("account_number")
        name_on_card = request.POST.get("name_on_card")
        
        try:
            order = Order.objects.get(id=order_id, customer=user, status="Pending")
            
            # Create Payment Record
            payment = Payment.objects.create(
                order=order,
                user=user,
                account_number=account_number[-4:], # Store only last 4 digits for demo security
                name_on_card=name_on_card,
                amount=order.amount
            )

            # Update Order Status
            order.status = "Paid"
            order.save()

            # Update Product Inventory
            cart_items = Cart.objects.filter(order=order)
            for item in cart_items:
                product = item.product
                if product.qty >= item.qnty:
                    product.qty -= item.qnty
                    product.save()
            
            messages.success(request, "Payment Successful! Thank you for your purchase.")
            return redirect("/user_home")

        except Order.DoesNotExist:
            messages.error(request, "Invalid Order")
            return redirect("/view_cart")

    return redirect("/view_cart")


# ==============================================================================
#                               ADMIN VIEWS
# ==============================================================================

def admin_home(request):
    """Admin Dashboard"""
    return render(request, "ADMIN/index.html")


def view_users(request):
    """Admin view all users"""
    if not request.user.is_authenticated or request.user.userType != "admin":
        return redirect("/login")

    users = User.objects.all()
    return render(request, "ADMIN/view_users.html", {"users": users})


def admin_user_details(request):
    """Admin view specific user details"""
    user_id = request.GET.get("id")
    if user_id:
        user = User.objects.get(id=user_id)
        drawings = Drawing.objects.filter(user=user)
        
        # Attach feedbacks to each drawing
        for d in drawings:
            d.feedbacks = DrawingFeedback.objects.filter(drawing=d).order_by('-date')
            
        return render(request, "ADMIN/user_details.html", {"user": user, "drawings": drawings})
    return redirect("/view_users")


def block_user(request):
    """Block a user"""
    user_id = request.GET.get("id")
    if user_id:
        user = User.objects.get(id=user_id)
        user.loginid.is_active = False
        user.loginid.save()
    return redirect(request.META.get('HTTP_REFERER', '/view_users'))


def unblock_user(request):
    """Unblock a user"""
    user_id = request.GET.get("id")
    if user_id:
        user = User.objects.get(id=user_id)
        user.loginid.is_active = True
        user.loginid.save()
    return redirect(request.META.get('HTTP_REFERER', '/view_users'))


def delete_user(request):
    """Delete a user account"""
    user_id = request.GET.get("id")
    if user_id:
        user = User.objects.get(id=user_id)
        user.loginid.delete()  # deletes login first
        user.delete()           # deletes user profile
    return redirect("/view_users")


def view_shops(request):
    """Admin view all shops"""
    if not request.user.is_authenticated or request.user.userType != "admin":
        return redirect("/login")

    shops = Shop.objects.all()
    return render(request, "ADMIN/view_shops.html", {"shops": shops})


def approve_shop(request):
    """Approve a shop registration"""
    shop_id = request.GET.get("id")
    if shop_id:
        shop = Shop.objects.get(id=shop_id)
        shop.status = "approved"
        shop.save()
        shop.loginid.is_active = True
        shop.loginid.save()
        messages.success(request, f"Shop {shop.name} approved successfully!")
    return redirect("/view_shops")


def reject_shop(request):
    """Reject a shop registration"""
    shop_id = request.GET.get("id")
    if shop_id:
        shop = Shop.objects.get(id=shop_id)
        shop.status = "rejected"
        shop.save()
        shop.loginid.is_active = False
        shop.loginid.save()
        messages.warning(request, f"Shop {shop.name} rejected.")
    return redirect("/view_shops")


def block_shop(request):
    """Block a shop"""
    shop_id = request.GET.get("id")
    if shop_id:
        shop = Shop.objects.get(id=shop_id)
        shop.status = "blocked"
        shop.save()
        shop.loginid.is_active = False
        shop.loginid.save()
    return redirect("/view_shops")


def unblock_shop(request):
    """Unblock a shop"""
    shop_id = request.GET.get("id")
    if shop_id:
        shop = Shop.objects.get(id=shop_id)
        shop.status = "approved"
        shop.save()
        shop.loginid.is_active = True
        shop.loginid.save()
    return redirect("/view_shops")


def admin_add_video(request):
    """Admin add tutorial video"""
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        video_link = request.POST.get("video_link")
        status = request.POST.get("status", "active")

        Video.objects.create(
            title=title,
            description=description,
            category=category,
            video_link=video_link,
            status=status
        )

        messages.success(request, "Video added successfully!")
        return redirect("/view_videos")

    return render(request, "ADMIN/add_video.html")


def view_videos(request):
    """Admin view all videos"""
    videos = Video.objects.all().order_by('-date')
    return render(request, "ADMIN/view_videos.html", {"videos": videos})


def delete_video(request):
    """Admin delete video"""
    video_id = request.GET.get("id")
    if video_id:
        try:
            video = Video.objects.get(id=video_id)
            video.delete()
        except Video.DoesNotExist:
            pass
    return redirect("/view_videos")


def admin_view_drawings(request):
    """Admin view all user drawings with feedback"""
    if not request.user.is_authenticated or request.user.userType != "admin":
        return redirect("/login")
        
    drawings = Drawing.objects.all().order_by('-date')
    
    # Attach feedbacks to each drawing
    for d in drawings:
        d.feedbacks = DrawingFeedback.objects.filter(drawing=d).order_by('-date')
        
    return render(request, "ADMIN/view_drawings.html", {"drawings": drawings})


def admin_view_feedback(request):
    """Admin view all user feedback (Products and Drawings)"""
    if not request.user.is_authenticated or request.user.userType != "admin":
        return redirect("/login")

    product_feedbacks = ProductFeedback.objects.all().order_by('-date')
    drawing_feedbacks = DrawingFeedback.objects.all().order_by('-date')
    
    return render(request, "ADMIN/view_feedback.html", {
        "product_feedbacks": product_feedbacks,
        "drawing_feedbacks": drawing_feedbacks
    })


def delete_product_feedback(request):
    """Admin delete product feedback"""
    if not request.user.is_authenticated or request.user.userType != "admin":
        return redirect("/login")

    fid = request.GET.get("id")
    if fid:
        ProductFeedback.objects.filter(id=fid).delete()
    return redirect("/view_feedback")

def delete_drawing_feedback(request):
    """Admin delete drawing feedback"""
    if not request.user.is_authenticated or request.user.userType != "admin":
        return redirect("/login")

    fid = request.GET.get("id")
    if fid:
        DrawingFeedback.objects.filter(id=fid).delete()
    return redirect(request.META.get('HTTP_REFERER', '/view_feedback'))


def my_orders(request):
    """User view their own orders"""
    if 'uid' not in request.session:
        return redirect("/login")

    user_login = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=user_login)

    orders = Order.objects.filter(customer=user).exclude(status="Pending").order_by('-date')
    return render(request, "USER/my_orders.html", {"orders": orders})


def user_order_details(request):
    """View details of a specific order"""
    if 'uid' not in request.session:
        return redirect("/login")

    oid = request.GET.get("id")
    order = get_object_or_404(Order, id=oid)
    cart_items = Cart.objects.filter(order=order)
    
    user_login = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=user_login)

    # Attach feedback object to each cart item if it exists
    for item in cart_items:
        item.feedback = ProductFeedback.objects.filter(product=item.product, user=user).first()

    return render(request, "USER/order_details.html", {"order": order, "cart_items": cart_items})


def add_product_feedback(request):
    """Add feedback for a purchased product"""
    if 'uid' not in request.session:
        return redirect("/login")

    pid = request.GET.get("pid")
    oid = request.GET.get("oid")
    
    product = get_object_or_404(Products, id=pid)
    order = get_object_or_404(Order, id=oid)
    
    user_login = Login.objects.get(id=request.session['uid'])
    user = User.objects.get(loginid=user_login)

    # Allow feedback only if order is Delivered
    if order.status != "Delivered":
        messages.error(request, "You can only rate delivered products.")
        return redirect(f"/user_order_details?id={oid}")

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Check if user already submitted feedback for this product
        if ProductFeedback.objects.filter(product=product, user=user).exists():
            messages.error(request, "You have already submitted feedback for this product.")
            return redirect(f"/user_order_details?id={oid}")

        ProductFeedback.objects.create(
            product=product,
            user=user,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Thank you for your feedback!")
        return redirect(f"/user_order_details?id={oid}")

    return render(request, "USER/add_product_feedback.html", {"product": product, "order": order})


def edit_product_feedback(request):
    """User edit own product feedback"""
    if 'uid' not in request.session:
        return redirect("/login")

    fid = request.GET.get("id")
    feedback = get_object_or_404(ProductFeedback, id=fid)

    # Ensure only the author can edit
    if feedback.user.loginid.id != request.session['uid']:
        messages.error(request, "You cannot edit this feedback.")
        return redirect("/my_orders")

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        if rating and comment:
            feedback.rating = rating
            feedback.comment = comment
            feedback.save()
            messages.success(request, "Feedback updated!")
            # We don't have the order id here easily, so redirect to my_orders
            return redirect("/my_orders")

    return render(request, "USER/edit_product_feedback.html", {"feedback": feedback})


def delete_product_feedback_user(request):
    """User delete own product feedback"""
    if 'uid' not in request.session:
        return redirect("/login")

    fid = request.GET.get("id")
    feedback = get_object_or_404(ProductFeedback, id=fid)

    # Ensure only the author can delete
    if feedback.user.loginid.id != request.session['uid']:
        messages.error(request, "You cannot delete this feedback.")
        return redirect("/my_orders")

    feedback.delete()
    messages.success(request, "Feedback deleted!")
    return redirect("/my_orders")
