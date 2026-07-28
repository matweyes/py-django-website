# Kitchen Service

A Django web application for managing a restaurant kitchen. Cooks can create
dishes and their types, and assign cooks responsible for preparing each dish.

## Features

- Authentication (login/logout) with all pages protected
- CRUD operations for Dishes, Dish Types, and Cooks
- Search functionality on all list pages (dishes by name, dish types by name, cooks by username)
- Assign/unassign cooks to dishes
- Pagination (5 items per page)
- Session-based visit counter on the home page
- Custom Cook model extending Django's AbstractUser with `years_of_experience` field
- Django Admin with customized CookAdmin

## Database structure

- **DishType**: `name`
- **Cook** (extends AbstractUser): `username`, `password`, `email`, `first_name`, `last_name`, `years_of_experience`
- **Dish**: `name`, `description`, `price`, `dish_type` (FK to DishType), `cooks` (M2M to Cook)

## How to run

### Prerequisites

- Python 3.10+

### Installation

```bash
git clone <repository-url>
cd py-django-website
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Seed the database (optional)

Populate the database with sample data using Faker:

```bash
python manage.py seed
```

Options:

| Flag | Description | Default |
|---|---|---|
| `--cooks N` | Number of cooks to create | 10 |
| `--dishes N` | Number of dishes to create | 30 |
| `--clear` | Clear existing data before seeding | off |

Examples:

```bash
python manage.py seed                          # 10 cooks, 30 dishes
python manage.py seed --cooks 5 --dishes 15    # custom amounts
python manage.py seed --clear                  # wipe & reseed
```

### Run the server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ and log in with your superuser credentials.

Admin panel is available at http://127.0.0.1:8000/admin/.

### Run tests

```bash
python manage.py test
```

### Run linter

```bash
flake8
```
