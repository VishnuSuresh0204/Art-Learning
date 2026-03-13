# Art Gallery Learning Platform

A comprehensive Django-based web application designed to bridge the gap between artists, art shops, and art enthusiasts. This platform allows artists to showcase their work, shops to manage their inventory, and users to discover and purchase unique art pieces.

## 🚀 Features

- **User Roles**: Specialized accounts for Artists, Shops, and regular Customers.
- **Artist Portfolio**: Artists can upload and manage their art gallery.
- **Shop Management**: Shop owners can register their business and list products.
- **Secure Authentication**: Robust registration and login system with integrity checks.
- **Interactive UI**: Modern, responsive design for a premium browsing experience.
- **Payment Integration**: Streamlined checkout process for art purchases.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Version Control**: Git

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/VishnuSuresh0204/Art-Learning.git
   cd art_gallary(3m)
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   cd art
   python manage.py migrate
   ```

5. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
