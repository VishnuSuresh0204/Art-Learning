from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # --- ADMIN/DJANGO ---
    path('admin/', admin.site.urls),

    # --- AUTHENTICATION ---
    path('', views.home),
    path('register/', views.register),
    path('shop_register/', views.shop_register),
    path('login/', views.login_view),
    path('about/', views.about),

    # --- USER PROFILE & NAVIGATION ---
    path('user_home/', views.user_home),
    path('shop_home/', views.shop_home),
    path('shop_add_product/', views.shop_add_product),
    path('shop_view_products/', views.shop_view_products),
    path('shop_edit_product/', views.shop_edit_product),
    path('shop_delete_product/', views.shop_delete_product),
    path('shop_view_bookings/', views.shop_view_bookings),
    path('shop_update_booking_status/', views.shop_update_booking_status),
    path('profile', views.profile),
    path('edit_profile', views.edit_profile),

    # --- USER DRAWINGS ---
    path('upload_drawing/', views.upload_drawing),
    path('view_drawings/', views.my_drawings),        # List own drawings
    path('all_drawings/', views.all_drawings),        # Gallery
    path('delete_drawing/', views.delete_drawing),
    path('drawing_detail', views.drawing_detail),
    path('edit_drawing/', views.edit_drawing, name='edit_drawing'),
    path('edit_feedback', views.edit_feedback),

    # --- USER SHOP & VIDEOS ---
    path("user_view_videos/", views.user_view_videos),
    path("user_view_products/", views.user_view_products),
    
    # --- USER CART ---
    path('add_to_cart', views.add_to_cart),
    path('view_cart', views.view_cart),
    path('remove_cart/', views.remove_cart),
    path('update_cart_quantity/', views.update_cart_quantity),
    path('checkout/', views.checkout),
    path('process_payment/', views.process_payment),

    # --- ADMIN: HOME & USERS ---
    path('admin_home/', views.admin_home),
    path("view_users/", views.view_users),
    path("user_details/", views.admin_user_details),
    path("block_user/", views.block_user),
    path("unblock_user/", views.unblock_user),
    path("delete_user/", views.delete_user),
    path("view_shops/", views.view_shops),
    path("approve_shop/", views.approve_shop),
    path("reject_shop/", views.reject_shop),
    path("block_shop/", views.block_shop),
    path("unblock_shop/", views.unblock_shop),

    # --- ADMIN: VIDEOS ---
    path("add_video/", views.admin_add_video),
    path("edit_video/", views.admin_edit_video),
    path("delete_video/", views.delete_video),
    path("view_videos/", views.view_videos),
    
    # --- ADMIN: PRODUCTS ---
    path("admin_view_drawings/", views.admin_view_drawings),
    
    # --- ADMIN: FEEDBACK ---
    path("view_feedback/", views.admin_view_feedback),
    path("delete_product_feedback/", views.delete_product_feedback),
    path("delete_drawing_feedback/", views.delete_drawing_feedback),

    # --- ORDERS ---
    path("my_orders/", views.my_orders),
    path("user_order_details/", views.user_order_details),
    path("add_product_feedback/", views.add_product_feedback),
    path("edit_product_feedback/", views.edit_product_feedback),
    path("delete_product_feedback_user/", views.delete_product_feedback_user),
    path("delete_drawing_feedback_user/", views.delete_drawing_feedback_user),

    # --- CHAT ---
    path('chat/<int:receiver_id>/', views.chat_view, name='chat_view'),
    path('send_message/', views.send_message, name='send_message'),
    path('my_chats/', views.my_chats, name='my_chats'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)