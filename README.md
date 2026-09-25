# 🚀 Mahak Qeshm Samaneh

### Modern Affiliate & Business Management Platform — Django + PWA

> A modern, responsive and scalable affiliate management platform built with **Django**, designed for managing users, products, orders, referrals, commissions, wallets and support services through a powerful RTL-ready Progressive Web App.

[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge\&logo=django\&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![PWA](https://img.shields.io/badge/PWA-Ready-5A0FC8?style=for-the-badge\&logo=pwa\&logoColor=white)](https://web.dev/progressive-web-apps/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge\&logo=html5\&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge\&logo=css3\&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge\&logo=javascript\&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

---

## 📌 Overview

**Mahak Qeshm Samaneh** is a full-stack web platform developed with Django and designed around a modern affiliate and business-management workflow.

The platform provides a centralized environment where administrators and users can manage:

* 👤 User accounts
* 🔗 Referral links and referral codes
* 📦 Products and packages
* 🛒 Orders
* 💰 Commissions
* 👛 Digital wallets
* 💸 Withdrawal requests
* 🎫 Support services
* 📊 User statuses and business categories
* 📱 Progressive Web App functionality
* 🛠️ Advanced administration tools

The interface is designed with a **modern RTL-first approach**, making it suitable for Persian-speaking users and business environments.

---

# ✨ Core Features

## 👤 User Management

Powerful user-management functionality for administrators.

### User Status Workflow

Users can move through different business states:

* 🔴 **Pending** — Newly registered and waiting for review
* 🟡 **Reviewed** — Verified by an administrator
* 🟢 **Purchased** — Completed a purchase

Administrators can also:

* Edit user information
* Change user status
* Record purchase dates
* Assign business categories
* Promote users to staff
* Perform bulk actions
* Filter users by status

---

## 🔗 Referral & Affiliate System

A built-in referral system makes it possible to track users and affiliate relationships.

### Referral Features

* Unique referral codes
* Personalized referral links
* Referral tracking
* Multi-level affiliate structure
* Commission management
* Automatic referral assignment
* Referral-based user registration

### Affiliate Levels

| Level     | Commission |
| --------- | ---------- |
| 🥉 Bronze | 5%         |
| 🥈 Silver | 10%        |
| 🥇 Gold   | 12%        |

The architecture is designed so that the affiliate system can be extended with additional levels and business rules.

---

# 💰 Wallet & Withdrawal System

Users can manage their earnings through an integrated wallet system.

### Wallet Features

* Wallet balance
* Commission income
* Withdrawal requests
* Withdrawal status tracking
* Admin approval workflow
* Transaction management

### Withdrawal States

```text
Pending
   ↓
Reviewed
   ↓
Approved
   ↓
Paid
```

Administrators can manage withdrawal requests directly from the Django administration panel.

---

# 📦 Product & Package Management

The platform provides a dedicated product/package management module.

Administrators can manage:

* Packages
* Package prices
* Product information
* User purchases
* Purchase history
* Package-related rewards
* Payment workflows

The architecture can also be extended to support external payment gateways such as Iranian payment providers.

---

# 🛒 Order Management

The order system is responsible for handling purchases and related affiliate commissions.

Typical workflow:

```text
User
 │
 ▼
Select Package
 │
 ▼
Create Order
 │
 ▼
Payment
 │
 ▼
Confirm Purchase
 │
 ├──► Update User Status
 │
 ├──► Calculate Commission
 │
 └──► Update Wallet
```

---

# 🎫 Support System

The platform includes a support-management module for handling service-related requests.

Users can request support services and administrators can manage their status through the administration panel.

This module can be expanded into a complete ticketing system with:

* Support tickets
* Ticket categories
* Priority levels
* Admin responses
* Ticket history
* Service renewal

---

# 📱 Progressive Web App

Mahak Qeshm Samaneh is designed with **PWA support**, allowing the web application to provide an app-like experience on supported devices.

### PWA Advantages

* 📱 Mobile-friendly interface
* ⚡ Fast loading experience
* 🖥️ Desktop support
* 📲 Installable web application
* 🔄 Responsive UI
* 🌐 Web-based deployment

---

# 🎨 UI / UX

The project follows a modern business-oriented interface with:

* RTL support
* Responsive layouts
* Mobile-first design
* Modern dashboard components
* Status badges
* Administrative tables
* Clean navigation
* PWA-ready interface

The project is particularly optimized for Persian-language users and RTL environments.

---

# 🧩 Project Architecture

The project follows a modular Django application architecture.

```text
mahak_qeshm_samaneh/
│
├── accounts/
│   └── User & Profile Management
│
├── products/
│   └── Products & Packages
│
├── orders/
│   └── Orders & Commissions
│
├── wallet/
│   └── Wallet & Withdrawals
│
├── referrals/
│   └── Referral & Affiliate System
│
├── support/
│   └── Support Services
│
├── affiliate_pwa/
│   └── Main Django Project
│
├── templates/
│   └── HTML Templates
│
├── static/
│   └── CSS, JavaScript & PWA Assets
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

### Backend

* 🐍 Python
* 🌐 Django
* 🔌 Django REST Framework
* 🔐 Django Authentication
* 🖼️ Pillow

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive Design
* RTL UI

### Application

* Progressive Web App (PWA)
* Django Admin
* Modular Architecture

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/GoldenIsland00/mahak_qeshm_samaneh.git

cd mahak_qeshm_samaneh
```

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements file configured yet:

```bash
pip install django djangorestframework django-cors-headers pillow python-decouple django-crispy-forms crispy-bootstrap5
```

---

# 🗄️ Database Setup

Run Django migrations:

```bash
python manage.py migrate
```

---

# 👑 Create an Administrator

Create your own Django superuser:

```bash
python manage.py createsuperuser
```

Then follow the prompts:

```text
Username:
Email:
Password:
Password confirmation:
```

---

# ▶️ Run the Development Server

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

---

# 🔐 Security Configuration

Before deploying the project to production, make sure to configure:

```python
DEBUG = False
```

Generate a secure production secret key and store sensitive configuration in environment variables.

Example:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
```

Never commit your real:

* `SECRET_KEY`
* Database credentials
* API keys
* Payment gateway credentials
* Private tokens

to GitHub.

---

# 💳 Payment Gateway

The payment architecture can be extended to support Iranian payment gateways.

For example:

```text
User
  ↓
Package Selection
  ↓
Create Order
  ↓
Payment Gateway
  ↓
Payment Verification
  ↓
Order Confirmation
  ↓
Commission Calculation
  ↓
Wallet Update
```

---

# 🔄 Business Workflow

```text
                    ┌───────────────┐
                    │     USER      │
                    └───────┬───────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Referral / Signup │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Admin Verification│
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Package Purchase  │
                  └─────────┬─────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
        ┌──────────────┐        ┌──────────────┐
        │    Order     │        │  Commission  │
        └──────┬───────┘        └──────┬───────┘
               │                       │
               └───────────┬───────────┘
                           ▼
                    ┌──────────────┐
                    │    Wallet    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Withdrawal  │
                    └──────────────┘
```

---

# 📊 Admin Dashboard

The administration system provides centralized control over the platform.

Administrators can manage:

* 👥 Users
* 📦 Products
* 🛒 Orders
* 💰 Commissions
* 👛 Wallets
* 💸 Withdrawals
* 🔗 Referrals
* 🎫 Support requests
* 🏷️ Business categories
* 📅 Purchase dates
* 🔐 Staff permissions

---

# 🚀 Future Roadmap

The project can be expanded with:

* [ ] Real payment gateway integration
* [ ] Advanced analytics dashboard
* [ ] Financial transaction reports
* [ ] SMS notifications
* [ ] Email notifications
* [ ] Push notifications
* [ ] Advanced referral analytics
* [ ] REST API
* [ ] Mobile application
* [ ] Automated commission calculation
* [ ] Advanced wallet transaction history
* [ ] Multi-language support
* [ ] Docker deployment
* [ ] Production CI/CD pipeline
* [ ] Automated testing
* [ ] Role-based permission management

---

# 🧪 Development

Run Django checks:

```bash
python manage.py check
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Collect static files:

```bash
python manage.py collectstatic
```

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/amazing-feature
```

3. Commit your changes

```bash
git commit -m "Add amazing feature"
```

4. Push the branch

```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request

---

# 🐛 Issues & Suggestions

If you discover a bug or have an idea for improving the platform, please open an issue in the repository.

When reporting a bug, include:

* Operating system
* Python version
* Django version
* Steps to reproduce
* Expected behavior
* Actual behavior
* Relevant error logs

---

# 📄 License

This project is currently maintained as a private/open development project.

Add an appropriate open-source license before distributing the project publicly.

---

# 👨‍💻 Developer

**GoldenIsland00**

Building modern web applications with Python, Django and modern web technologies.

---

<div align="center">

### ⚡ Built with Python & Django

**Mahak Qeshm Samaneh**

Modern • Modular • Responsive • PWA Ready

⭐ Star the repository if you find it useful!

</div>
