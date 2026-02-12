# 📦 Requirements & Dependencies

## What is `requirements.txt`?

It's a plain text file that lists **every Python package your project needs**, along with exact version numbers. This is how other developers (or your future self) can recreate your exact environment.

Example `requirements.txt`:
```
Django==6.0.2
djangorestframework==3.16.1
mongoengine==0.29.1
```

---

## Installing Packages

### Install a single package:
```bash
pip install django
```

### Install a specific version:
```bash
pip install django==6.0.2
```

### Install everything from `requirements.txt`:
```bash
pip install -r requirements.txt
```

> ⚠️ **Always activate your virtual environment first!** Otherwise packages install globally.

---

## Generating `requirements.txt`

After you've installed all the packages you need, run:

```bash
pip freeze > requirements.txt
```

**What this does:**
- `pip freeze` — Lists all installed packages with their versions
- `> requirements.txt` — Writes that list to a file

### Example output of `pip freeze`:
```
asgiref==3.11.1
Django==6.0.2
django-cors-headers==4.9.0
django-rest-framework-mongoengine==3.4.1
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
dnspython==2.8.0
mongoengine==0.29.1
PyJWT==2.11.0
pymongo==4.16.0
python-dotenv==1.2.1
sqlparse==0.5.5
tzdata==2025.3
mongomock
werkzeug
```

---

## What Each Dependency Does

Here are the key packages used in this project:

| Package | What it does |
|---------|-------------|
| `Django` | The web framework itself — handles routing, middleware, settings, etc. |
| `djangorestframework` | Adds REST API capabilities to Django — `APIView`, `Response`, `Serializers`, permissions |
| `mongoengine` | ODM (Object Document Mapper) for MongoDB — like Django's ORM but for MongoDB |
| `django-rest-framework-mongoengine` | Bridge between DRF serializers and MongoEngine documents |
| `djangorestframework-simplejwt` | JWT token generation, validation, and refresh logic |
| `pymongo` | Low-level MongoDB driver (MongoEngine uses this under the hood) |
| `dnspython` | Required for `mongodb+srv://` connection strings |
| `python-dotenv` | Loads environment variables from a `.env` file into `os.getenv()` |
| `django-cors-headers` | Allows your frontend (different origin) to talk to your backend |
| `werkzeug` | Provides `generate_password_hash` and `check_password_hash` for secure password hashing |
| `PyJWT` | Core JWT library (SimpleJWT uses this internally) |
| `mongomock` | In-memory MongoDB mock for testing without a real database |
| `asgiref` | Async support for Django (installed automatically with Django) |
| `sqlparse` | SQL parser (Django dependency, not used with MongoDB) |

---

## Tips

### Check what's installed:
```bash
pip list
```

### Upgrade a package:
```bash
pip install --upgrade django
```

### Uninstall a package:
```bash
pip uninstall django
```

### Regenerate after changes:
```bash
pip freeze > requirements.txt
```

> **Best practice:** Run `pip freeze > requirements.txt` every time you add or remove a package, then commit the updated file to Git.

---

## 🔗 Navigation

← **[Previous: Virtual Environments](./virtual_environments.md)**

← **[Back to Learning Django](../learning_django.md)**

→ **Next: [Setting Up Your First Django Project](./setting_up_django_project.md)**
