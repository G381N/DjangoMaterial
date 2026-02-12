# ⚙️ Step 2: Settings & Configuration

This step covers configuring `settings.py` — loading environment variables, registering apps and middleware, setting up DRF, JWT, CORS, and initializing the database connection.

> **By the end of this step, you'll have:** A fully configured Django project ready to connect to MongoDB Atlas with JWT authentication enabled.

---

## 2.1 Import Necessary Modules

At the top of `ProjectManagerCore/settings.py`, add these imports:

```python
from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
```

| Import | Why |
|--------|-----|
| `Path` | Clean file path handling (`BASE_DIR`) |
| `os` | Access environment variables via `os.getenv()` |
| `timedelta` | Set JWT token lifetimes (e.g., 30 minutes) |
| `load_dotenv` | Loads variables from the `.env` file |

---

## 2.2 Load Environment Variables

```python
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

MONGO_URI = os.getenv("CONNECTION_STRING") or os.getenv("MONGO_URI")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:8080")
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-change-this')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
```

**What's happening:**
- `BASE_DIR` → The project root directory (where `manage.py` lives)
- `load_dotenv(BASE_DIR / ".env")` → Reads your `.env` file and makes its values available via `os.getenv()`
- `SECRET_KEY` → Used by Django + JWT for cryptographic signing. **Keep this secret!**
- `DEBUG = True` → Shows detailed error pages in development. **Set to `False` in production!**
- `ALLOWED_HOSTS` → Which domains can access the app (`*` = all, for development)

---

## 2.3 Register Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'rest_framework',                # Django REST Framework
    'rest_framework_mongoengine',    # DRF ↔ MongoEngine bridge
    'corsheaders',                   # CORS support

    # local apps
    'auth_handler',                  # Our authentication app
    'project_handler',               # Our projects & tasks app
]
```

> ⚠️ **Order matters for CORS!** `corsheaders` must be in `INSTALLED_APPS` and its middleware must be at the **top** of `MIDDLEWARE`.

---

## 2.4 Configure Middleware

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',         # ← MUST be first!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Why CORS middleware is first:** It needs to add CORS headers to responses **before** any other middleware processes the request. If it's lower in the list, preflight requests might get blocked.

> 📖 **What is CORS?** When your frontend (`localhost:8080`) tries to call your backend (`localhost:8000`), the browser blocks it by default because they're different "origins". CORS headers tell the browser it's okay.

---

## 2.5 Configure Django REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth_handler.backends.MongoJWTAuthentication',   # Our custom JWT backend
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',     # Require login by default
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

**What each setting does:**

| Setting | Effect |
|---------|--------|
| `DEFAULT_AUTHENTICATION_CLASSES` | Every request is checked through `MongoJWTAuthentication` — which reads the JWT from the `Authorization` header and fetches the user from MongoDB |
| `DEFAULT_PERMISSION_CLASSES` | Every view requires login **by default**. Public views (login, register) override this with `AllowAny` |
| `DEFAULT_PAGINATION_CLASS` | List endpoints automatically paginate results |
| `PAGE_SIZE` | 10 results per page |

> `MongoJWTAuthentication` is the custom backend we'll create in **[Step 4 — Auth Module](./steps_auth_module.md)**.

---

## 2.6 Configure SimpleJWT

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),   # Short-lived
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),       # Long-lived
    'AUTH_HEADER_TYPES': ('Bearer',),                  # Header format
}
```

| Setting | Value | Meaning |
|---------|-------|---------|
| `ACCESS_TOKEN_LIFETIME` | 30 minutes | How long an access token is valid |
| `REFRESH_TOKEN_LIFETIME` | 7 days | How long a refresh token is valid |
| `AUTH_HEADER_TYPES` | `Bearer` | Clients must send: `Authorization: Bearer <token>` |

> 📖 See **[Learning → JWT Authentication](../learning/jwt_explained.md)** for how access/refresh tokens work.

---

## 2.7 Configure CORS

```python
CORS_ALLOWED_ORIGINS = [FRONTEND_ORIGIN]
```

This allows your frontend origin (loaded from `.env`, defaults to `http://localhost:8080`) to make API calls to this backend.

---

## 2.8 Initialize the Database Connection

```python
# At the bottom of settings.py:
try:
    from .db import init_db
    init_db()
except Exception:
    pass
```

This calls `init_db()` from `db.py` (which we'll create in the next step) as soon as Django starts up. It wraps in `try/except` so the app doesn't crash if MongoDB is unavailable.

> 📖 See **[Step 3 — Database Connection](./my_project_db.md)** for what `init_db()` does.

---

## 2.9 Other Standard Settings

These are the default Django settings you typically don't change:

```python
ROOT_URLCONF = 'ProjectManagerCore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProjectManagerCore.wsgi.application'

# Django's default SQL database (needed for Django internals, not for our app data)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

> **Why is SQLite still here?** Django's internal systems (admin, sessions, content types) still expect a SQL database. We keep the default SQLite for that. Our **app data** (users, projects, tasks) goes to MongoDB through MongoEngine.

---

## ✅ Complete `settings.py`

<details>
<summary>Click to expand the full file</summary>

```python
from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

MONGO_URI = os.getenv("CONNECTION_STRING") or os.getenv("MONGO_URI")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:8080")
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-nowtvc&7^rz6-vw#$c$vf&a8sz@*158cpid6q^b=z_z7zoso53')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'rest_framework',
    'rest_framework_mongoengine',
    'corsheaders',

    # local apps
    'auth_handler',
    'project_handler',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProjectManagerCore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProjectManagerCore.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth_handler.backends.MongoJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

CORS_ALLOWED_ORIGINS = [FRONTEND_ORIGIN]

try:
    from .db import init_db
    init_db()
except Exception:
    pass

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

</details>

---

## 🔗 Navigation

← **[Previous: Step 1 — Scaffolding](./my_project_scaffolding.md)**

← **[Back to My Django Project](../my_django_project.md)**

→ **Next: [Step 3 — Database Connection (db.py)](./my_project_db.md)**
