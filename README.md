# 🛠️ Freelance Service Marketplace API

A Django REST Framework (DRF) powered backend for a freelance service marketplace.  
It supports role-based access (Buyer, Seller, Admin), service management, order tracking, reviews, and dashboards.  
Integrated with **Swagger/OpenAPI** documentation for easy API exploration.  

---

## 🚀 Features

### 🔐 Authentication & Roles
- JWT Authentication  
- Roles: **Buyer, Seller, Admin**  
- Role-based permissions  

### 🛍️ Services
- Sellers can create, update, delete their services  
- Buyers & Guests can browse active services  
- Search & Filter services (by title, description, category, price)  
- Upload service images  
- Write & manage reviews  

### 📦 Orders
- Buyers can place orders for services  
- Sellers can manage received orders  
- Role-based order status updates:
  - Buyer → can **only cancel** their orders  
  - Seller → can **approve/complete** orders  
  - Admin → can manage all orders  

### 📊 Dashboards
- **Seller Dashboard**: services, earnings, reviews, orders  
- **Buyer Dashboard**: order history, reviews, spending  

### 📖 API Documentation
- Integrated with **Swagger UI** via `drf-yasg`  
- Each endpoint includes **summary, description, request body, and responses**  

---

## ⚙️ Tech Stack

- **Backend**: Django 5.x, Django REST Framework  
- **Database**: PostgreSQL (recommended) / SQLite (development)  
- **Auth**: JWT Authentication (`djangorestframework-simplejwt`)  
- **Docs**: Swagger (drf-yasg)  
- **Filters/Search**: django-filter  

---

