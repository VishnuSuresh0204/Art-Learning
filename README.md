# 🎨 Art Learning Platform

A full-stack Django web application that connects artists and art enthusiasts — enabling them to share artwork, communicate, buy art supplies, and access tutorials.

---

## ✨ Features

### 👤 Users
- Register, log in, and manage their profile
- Upload and manage personal artwork (drawings)
- Browse a public art gallery
- Add feedback/comments on other users' drawings
- **Chat directly with artists** about their work
- View and buy products from the shop
- Track order history

### 🛒 Shop (Artists/Sellers)
- Register as a shop (requires admin approval)
- Add, edit, and delete products
- Manage and update order/booking statuses

### 🔐 Admin
- Approve, block, or reject shop registrations
- Manage users (view, block, unblock, delete)
- Add and manage tutorial videos (YouTube links)
- View and delete drawing & product feedback

---

## 🗂️ Project Structure

```
art_gallary/
├── art/
│   ├── myapp/
│   │   ├── models.py        # Database models
│   │   ├── views.py         # All view logic
│   │   ├── migrations/      # Database migrations
│   │   └── admin.py
│   ├── art/
│   │   └── urls.py          # URL routing
│   ├── templates/
│   │   ├── USER/            # User-facing templates
│   │   ├── SHOP/            # Shop-facing templates
│   │   └── ADMIN/           # Admin templates
│   ├── static/              # CSS, JS, images
│   └── media/               # User uploaded files
└── README.md
```

---

## 🗄️ Models

| Model | Description |
|-------|-------------|
| `Login` | Custom user model (extends AbstractUser) |
| `User` | User profile (name, email, phone, image) |
| `Shop` | Shop profile (requires admin approval) |
| `Drawing` | Artwork uploaded by users |
| `DrawingFeedback` | Comments on drawings |
| `Video` | Tutorial videos (YouTube links) added by admin |
| `Products` | Art supplies/products listed by shops |
| `Order` | Customer order (groups cart items) |
| `Cart` | Individual product entries in an order |
| `Payment` | Payment records |
| `ProductFeedback` | Ratings and reviews for products |
| `Chat` | User-to-user messages |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/VishnuSuresh0204/Art-Learning.git
cd Art-Learning

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install django pillow

# 4. Apply migrations
cd art
python manage.py migrate

# 5. Create a superuser (Admin)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 💬 Chat System

Users can initiate chats directly from a drawing's detail page by clicking **"Chat with Artist"**. All active conversations are accessible from the **Messages** link in the navigation menu.

---

## 🔑 User Roles

| Role | Default Path | Notes |
|------|-------------|-------|
| Admin | `/admin_home/` | Use Django createsuperuser |
| Shop | `/shop_home/` | Requires admin approval |
| User | `/user_home/` | Self-registration |

---

## 🛠️ Built With

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, Bootstrap 4
- **Database:** SQLite (default)
- **Media:** Pillow (image handling)

---

## 📄 License

This project is for educational purposes.
