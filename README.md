# Comment-Board-BE 🗨️

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.7-0C4B33?logo=django&logoColor=white)](https://docs.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.16.1-ff1709?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
[![CAPTCHA](https://img.shields.io/badge/CAPTCHA-django--simple--captcha-4B8BBE)](https://github.com/mbi/django-simple-captcha)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

Backend for a single‑page application that manages threaded comments with file uploads. It provides a clean REST API with nested replies, XSS‑safe content, CAPTCHA validation, optional anonymous JWT access, and Dockerized deployment.

---

## ✨ Core Features

- Comments API (Django REST Framework)
  - Threaded/nested replies with recursive serialization
  - Create/list/retrieve/update/delete root comments and replies
  - Server‑side pagination for root comments
- File uploads
  - Images (JPG/PNG/GIF) and text (.txt) attachments
  - Size/type validation (text files ≤ 100 KB)
- Security
  - HTML sanitization of comment text (XSS protection)
  - CAPTCHA verification on comment create
  - Optional long‑lived anonymous JWT token for public clients
  - CORS configured for local frontend (http://localhost:3000)
- DevOps
  - Docker Compose for API and PostgreSQL
  - Environment‑driven configuration via django‑environ

---

## 🧰 Tech Stack

- Language: Python 3.13
- Framework: Django 5.2.7
- API: Django REST Framework 3.16
- Auth: djangorestframework‑simplejwt (JWT)
- CAPTCHA: django‑simple‑captcha
- Database: PostgreSQL
- Static/Media: Django file storage (media/)
- Packaging: Poetry
- Web server (prod): Gunicorn (container)

---

## ⚙️ Installation & Setup

1) Clone the repository

```bash
git clone https://github.com/Zebaro24/Comment-Board-BE.git
cd Comment-Board-BE
```

2) Install dependencies with Poetry

```bash
poetry install
```

3) Create an .env file at the project root

```dotenv
# Required
SECRET_KEY=change-me
DEBUG=true

# Database (defaults shown)
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=comment-board-db

# Optional
# Adjust CORS in settings.py if needed (CORS_ALLOWED_ORIGINS)
```

4) Apply migrations and run the server

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver 0.0.0.0:8000
```

The API will be available at http://127.0.0.1:8000/.

---

## 🚀 Quick Start (Docker Compose)

This project includes a docker-compose.yml to spin up PostgreSQL and the backend.

```bash
# Ensure you created an .env (see above) or export the variables
docker compose -p comment-board up -d --build
```

Services started:
- comment-board-db (PostgreSQL)
- comment-board-be (Django app on port 8000)

The app will wait for the database to be healthy and then start. Access http://localhost:8000/.

---

## 🧭 Running Locally (without Docker)

1) Ensure PostgreSQL is running and accessible (see .env values).
2) Activate Poetry environment and run:

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Optional: create a superuser for Django admin.

```bash
poetry run python manage.py createsuperuser
```

---

## 🔌 API Overview

Base URL: http://localhost:8000/

- Comments
  - GET /comments/ — list paginated root comments (with nested replies and files)
  - POST /comments/ — create a comment or reply
    - Body (multipart/form-data if uploading files):
      - username (string, alphanumeric)
      - email (email)
      - homepage (url, optional)
      - text (HTML allowed but sanitized)
      - parent (integer, optional — ID of parent comment)
      - captcha (string, format "<key>:<answer>")
      - file (optional, repeatable) — images (jpg/png/gif) or text (.txt ≤ 100KB)
  - GET /comments/{id}/ — retrieve a single root comment with nested replies
  - PUT/PATCH /comments/{id}/ — update a comment (auth required)
  - DELETE /comments/{id}/ — delete a comment (auth required)

- CAPTCHA
  - GET /captcha/ — returns a JSON with a generated CAPTCHA key and absolute image URL
    - Response example:
      ```json
      {"key":"<hashkey>","image":"http://localhost:8000/captcha/image/<hashkey>/"}
      ```

- Anonymous Token
  - POST /token-anon/ — returns a long‑lived JWT access token for the built‑in anon user
    - Response: `{ "token": "<jwt>" }`

Notes:
- For endpoints requiring authentication, include the token:
  - Header: `Authorization: Bearer <token>`
- Root comments are paginated; replies are fully embedded recursively.

---

## 🧪 Validation & Rules

- Username: only Latin letters and digits
- Email: must be a valid email
- Homepage: must be a valid URL if provided
- Text: sanitized to allow only a safe subset of HTML
- Files:
  - Images: .jpg/.jpeg/.png/.gif
  - Text: .txt only, size ≤ 100 KB

Uploaded files are stored under media/uploads/.

---

## 🔧 Configuration Reference

Environment variables (via .env):
- SECRET_KEY: Django secret key
- DEBUG: true/false (never enable in production)
- DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME: PostgreSQL settings

Project settings highlights:
- CORS_ALLOWED_ORIGINS: defaults to http://localhost:3000 (adjust as needed)
- MEDIA_ROOT: ./media, MEDIA_URL: /media/
- REST auth: JWT (SimpleJWT). Anonymous token endpoint is provided for convenience.

---

## 🧪 Testing

Use Django’s test runner:

```bash
poetry run python manage.py test
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## 📬 Contact

- Author: Zebaro
- Email: denok100100@gmail.com
