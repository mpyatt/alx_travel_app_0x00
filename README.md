# 🧭 ALX Travel App

A real-world Django-based backend service for managing travel listings, designed with scalability, documentation, and developer experience in mind.

## 🚀 Features

- Django REST API with modular app structure (`listings`)
- MySQL as the primary database (configured via `django-environ`)
- Swagger API docs at `/swagger/` using `drf-yasg`
- CORS enabled for secure cross-origin API requests
- Docker + Docker Compose setup for easy deployment
- Celery-ready for background task processing

---

## 📦 Requirements

- Python 3.10+ (recommended via `pyenv`)
- Docker & Docker Compose
- MySQL 8 (containerized)
- Virtualenv (`python -m venv .venv`)

---

## 🛠️ Local Development Setup

```bash
# Clone the repo
git clone https://github.com/your-username/alx_travel_app.git
cd alx_travel_app

# Create and activate virtual environment
pyenv local 3.10.12
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env  # then edit as needed

# Start MySQL in Docker
docker-compose up -d db

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
````

---

## 🐳 Docker Setup

To run the full stack in Docker:

```bash
docker-compose up --build
```

This will start:

* `api` container running Django + Gunicorn
* `db` container running MySQL

---

## 🔐 Environment Variables

Add a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=alxtravel
DB_USER=alxuser
DB_PASSWORD=alxpass
DB_HOST=db
DB_PORT=3306
```

> Don't commit this file — it's already in `.gitignore`

---

## 📚 API Documentation

* Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* Automatically generated using `drf-yasg`

---

## 🧪 Testing

```bash
python manage.py test
```

---

## 🧱 Project Structure

```
alx_travel_app/
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
├── README.md
├── manage.py
├── alx_travel_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── listings/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── migrations/
│       └── __init__.py
```

---

## 📌 Credits

Built as part of the **ALX Software Engineering Program** to demonstrate Django best practices, MySQL integration, and production-grade API architecture.
