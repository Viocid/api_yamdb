# API Yamdb

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-3.2-092E20)
![DRF](https://img.shields.io/badge/DRF-REST%20API-red)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Pytest](https://img.shields.io/badge/Pytest-tested-green)

API Yamdb is a collaborative REST API platform for collecting reviews, ratings and comments for different works such as books, movies and music.

The project was developed as a team backend project. My role included backend development and team lead responsibilities.

---

## Main features

- User registration by email and username
- Confirmation code based authentication flow
- JWT token authentication
- User roles: user, moderator and admin
- Category and genre management
- Title management
- Reviews for titles
- Nested comments for reviews
- Rating calculation logic through reviews
- Role-based permissions
- Filtering by category, genre, name and year
- Redoc API documentation
- Automated tests with Pytest

---

## My role

**Team Lead / Backend Developer**

Responsibilities included:

- decomposing tasks between team members;
- coordinating Git workflow;
- reviewing pull requests;
- resolving integration issues;
- implementing backend features;
- maintaining API consistency;
- working with user model, roles and permissions.

---

## Tech stack

- Python
- Django
- Django REST Framework
- Simple JWT
- Django Filter
- Pytest
- SQLite / PostgreSQL-compatible Django ORM setup

---

## Project structure

```text
api_yamdb/
├── api/                    # API viewsets, serializers, filters and permissions
├── api_yamdb/              # Django project settings and root URLs
├── custom_users/           # Custom user model, auth and role logic
├── reviews/                # Categories, genres, titles, reviews and comments
├── static/redoc.yaml       # API documentation schema
├── templates/redoc.html    # Redoc page
└── manage.py
```

---

## API endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/signup/` | Register user and receive confirmation code |
| `POST` | `/api/v1/auth/token/` | Get JWT token |

### Users

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/users/` | Get users list |
| `POST` | `/api/v1/users/` | Create user |
| `GET` | `/api/v1/users/{username}/` | Get user profile |
| `PATCH` | `/api/v1/users/{username}/` | Update user profile |
| `DELETE` | `/api/v1/users/{username}/` | Delete user |

### Categories, genres and titles

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/categories/` | Get categories |
| `POST` | `/api/v1/categories/` | Create category |
| `DELETE` | `/api/v1/categories/{slug}/` | Delete category |
| `GET` | `/api/v1/genres/` | Get genres |
| `POST` | `/api/v1/genres/` | Create genre |
| `DELETE` | `/api/v1/genres/{slug}/` | Delete genre |
| `GET` | `/api/v1/titles/` | Get titles |
| `POST` | `/api/v1/titles/` | Create title |
| `GET` | `/api/v1/titles/{id}/` | Get title details |
| `PATCH` | `/api/v1/titles/{id}/` | Update title |
| `DELETE` | `/api/v1/titles/{id}/` | Delete title |

### Reviews and comments

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/titles/{title_id}/reviews/` | Get title reviews |
| `POST` | `/api/v1/titles/{title_id}/reviews/` | Create review |
| `GET` | `/api/v1/titles/{title_id}/reviews/{review_id}/` | Get review |
| `PATCH` | `/api/v1/titles/{title_id}/reviews/{review_id}/` | Update review |
| `DELETE` | `/api/v1/titles/{title_id}/reviews/{review_id}/` | Delete review |
| `GET` | `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` | Get comments |
| `POST` | `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` | Create comment |

---

## Local installation

Clone the repository:

```bash
git clone https://github.com/Viocid/api_yamdb.git
cd api_yamdb
```

Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Go to the Django project directory:

```bash
cd api_yamdb
```

Apply migrations:

```bash
python manage.py migrate
```

Run development server:

```bash
python manage.py runserver
```

API documentation:

```text
http://127.0.0.1:8000/redoc/
```

---

## Running tests

From the repository root:

```bash
pytest
```

---

## What this project demonstrates

- Team backend development
- Django REST Framework viewsets and routers
- Nested API resources
- JWT authentication
- Role-based permissions
- Custom user model
- Filtering and validation
- Test-driven project requirements
- Code review and task coordination experience

