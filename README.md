# 📘 User Management Service (Flask Backend)

This project is a **Flask-based User Management API** that demonstrates core backend concepts including authentication, authorization, database management, caching, rate limiting, and asynchronous task processing.

---

## 🚀 Features Implemented

### 1. User Management APIs (CRUD)

* Built RESTful APIs for user operations:

  * Create User
  * Read User(s)
  * Update User
  * Delete User
* Follows clean architecture and modular design using Flask Blueprints.

---

### 2. SQLite Database Integration

* User data is persisted using **SQLite**.
* Integrated with **SQLAlchemy ORM** for:

  * Easy database interactions
  * Model-based schema design
* Supports migrations using Flask-Migrate.

---

### 3. JWT Authentication & RBAC

* Implemented **JWT (JSON Web Token)** based authentication.
* Secured endpoints using access tokens.
* Role-Based Access Control (RBAC):

  * Admin vs Normal User access
  * Protected routes using decorators

---

### 4. Secure Password Storage

* User passwords are **hashed and encrypted** before storing in the database.
* Used libraries like:

  * `bcrypt` or `werkzeug.security`
* Ensures:

  * No plain-text password storage
  * Protection against common attacks

---

### 5. Redis Cache & Celery Integration

* Integrated **Redis** for:

  * Caching frequently accessed data
  * Improving API performance
* Integrated **Celery** for asynchronous task processing:

  * Background jobs (e.g., sending emails)
  * Non-blocking API responses

---

### 6. Rate Limiting (API Protection)

* Implemented **rate limiting** using Flask-Limiter.
* Prevents abuse by restricting the number of requests per user/IP.
* Helps protect against:

  * Brute-force attacks
  * API flooding
* Configurable limits (e.g., requests per minute/hour)

---

### 7. Dockerize this application

* Implemented Dockerfile and .dockerignore
* Implemented docker-compose.yaml which contains three services
  * web
  * redis
  * celery

---

## ⚙️ Tech Stack

* **Backend:** Flask
* **Database:** SQLite
* **Authentication:** JWT
* **Caching:** Redis
* **Async Tasks:** Celery
* **Rate Limiting:** Flask-Limiter
* **ORM:** SQLAlchemy
* **Docker**

---

## 📌 Future Enhancements

* Deploy on cloud (AWS/GCP)

---

## 🧠 Learning Outcomes

* Built a production-style Flask backend
* Understood async processing using Celery
* Implemented secure authentication & authorization
* Improved performance using caching
* Secured APIs using rate limiting

---

## ▶️ How to Run without Docker

```bash id="8t8y4p"
# Install dependencies
pip install -r requirements.txt

# Run Redis
redis-server

# Run Flask app
python3 run.py

# Start Celery worker
celery -A app.celery_app.celery worker --loglevel=info
```
## ▶️ How to Run without Docker
```
# Run docker-compose.yml
docker-compose up --build

# Set Up the DB
docker-compose exec web python3 -m setup_db

# Create Admin User
docker-compose exec web python3 -m app.create_admin
```

---

## 📬 Author

Developed as part of backend learning and system design practice.
