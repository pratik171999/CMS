
# Content Management System (CMS) API

This repository contains the API for a Content Management System (CMS) built with Django and Django Rest Framework. The API supports user registration, login, content creation, and search functionalities.

## Requirements

Before setting up the project, ensure that you have the following installed on your local machine:

- Python 3.8 or higher
- Django 3.0 or higher
- Django Rest Framework (DRF)
- Virtual Environment tool (like `virtualenv` or `venv`)

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

git clone <repository-url>
cd <repository-directory>

### 2. Create and Activate Virtual Environment

Create a virtual environment and activate it:

#### On Windows:
python -m venv venv
\env\Scripts\ctivate


#### On macOS/Linux:
python3 -m venv venv
source venv/bin/activate


### 3. Install Dependencies

Install the required dependencies listed in the `requirements.txt`:

pip install -r requirements.txt

### 4. Configure Database

Ensure your PostgreSQL (or other database) is running and set up the database for this project. You can update the database configuration in `settings.py` under the `DATABASES` section.

If using PostgreSQL, the `DATABASES` configuration in `settings.py` should look like this:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cms_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

### 5. Apply Migrations

Run the following commands to apply database migrations:

python manage.py migrate


### 6. Run the Development Server

Run the Django development server to start the API:

python manage.py runserver


The server will start on `http://127.0.0.1:8000/`. You can now access the API and perform requests.

### 7. Run Test Cases

To run the test cases, use the following command:

python manage.py test

This will automatically find all the test cases in the `tests.py` file and execute them.

#### Test Cases

- **User Registration**: Tests if the user (author and admin) can register successfully.
- **Login**: Tests if the user can log in and get a JWT token.
- **Content Creation**: Tests if an authenticated user can create content items.
- **Content Search**: Tests the search functionality for content by title and body.
  
If the tests pass, you should see output similar to:

Ran 8 tests in 14.832s
FAILED (failures=0)


## API Endpoints

### 1. **User Registration**
- `POST /api/register/`
  - Request body: 
    ```json
    {
      "email": "user@example.com",
      "username": "user",
      "password": "password123",
      "phone": "1234567890",
      "address": "Some Address",
      "city": "Some City",
      "state": "Some State",
      "country": "Some Country",
      "pincode": "123456"
    }
    ```
  - Response: 201 Created

### 2. **Login**
- `POST /login/`
  - Request body:
    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```
  - Response: 
    ```json
    {
      "access": "your-jwt-token"
    }
    ```

### 3. **Create Content**
- `POST /api/content/`
  - Request body:
    ```json
    {
      "title": "Sample Content",
      "body": "This is the body of the content.",
      "summary": "Short summary",
      "categories": [1]
    }
    ```
  - The `document` field is a file upload (PDF format).
  - Authentication: JWT token in the `Authorization` header.

### 4. **Search Content**
- `GET /api/content/?search=sample`
  - Request: Search for content by title or body.
  - Response: A list of content matching the search query.

## Project Structure

```
cms_project/
├── cms_app/                # Application containing models and views
│   ├── migrations/
│   ├── models.py           # Models for content items, categories, etc.
│   ├── serializers.py      # Serializers for data validation
│   ├── tests.py            # Test cases for API endpoints
│   └── views.py            # Views for handling API requests
├── cms_project/            # Project configuration files
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routes for the API
│   └── wsgi.py
└── manage.py               # Django management script
```

