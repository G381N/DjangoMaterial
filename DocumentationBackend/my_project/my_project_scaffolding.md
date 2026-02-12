# 🏗️ Step 1: Scaffolding the Project

This step covers setting up the project skeleton — the virtual environment, installing all packages, creating the Django project and apps, environment variables, and generating `requirements.txt`.

> **By the end of this step, you'll have:** A running Django project with two empty apps and all dependencies installed.

---

## 1.1 Create the Project Folder

```bash
mkdir "ProjectManager Backend"
cd "ProjectManager Backend"
```

---

## 1.2 Create & Activate Virtual Environment

```bash
python -m venv venv
```

**Activate it:**
```bash
# Windows (PowerShell)
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

> 📖 See **[Learning → Virtual Environments](../learning/virtual_environments.md)** for a full explanation.

---

## 1.3 Install All Dependencies

Install the packages one by one (so you understand what each one is for):

```bash
# The web framework
pip install django

# REST API capabilities
pip install djangorestframework

# MongoDB ODM
pip install mongoengine

# Bridge DRF serializers with MongoEngine
pip install django-rest-framework-mongoengine

# JWT authentication
pip install djangorestframework-simplejwt

# Load secrets from .env files
pip install python-dotenv

# Allow frontend to talk to backend (CORS)
pip install django-cors-headers

# DNS support for MongoDB Atlas connection strings
pip install dnspython

# Password hashing
pip install werkzeug

# In-memory MongoDB mock for testing
pip install mongomock
```

**Or install everything at once:**
```bash
pip install django djangorestframework mongoengine django-rest-framework-mongoengine djangorestframework-simplejwt python-dotenv django-cors-headers dnspython werkzeug mongomock
```

> 📖 See **[Learning → Requirements & Dependencies](../learning/requirements_and_dependencies.md)** for what each package does.

---

## 1.4 Create the Django Project

```bash
django-admin startproject ProjectManagerCore .
```

> **Important:** The `.` at the end creates the project **in the current directory** (no extra nesting).

**Your folder now looks like:**
```
ProjectManager Backend/
├── manage.py
├── venv/
└── ProjectManagerCore/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

---

## 1.5 Create the Apps

```bash
python manage.py startapp auth_handler
python manage.py startapp project_handler
```

**Your folder now has:**
```
ProjectManager Backend/
├── manage.py
├── venv/
├── ProjectManagerCore/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── auth_handler/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── migrations/
└── project_handler/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── views.py
    └── migrations/
```

---

## 1.6 Create the `.env` File

Create a file called `.env` in the project root (same level as `manage.py`):

```ini
CONNECTION_STRING=mongodb+srv://<username>:<password>@cluster.mongodb.net/
SECRET_KEY=your-secret-key-here
```

Replace `<username>` and `<password>` with your MongoDB Atlas credentials.

> ⚠️ **Never commit `.env` to Git!** Add it to `.gitignore`:
> ```
> .env
> venv/
> __pycache__/
> db.sqlite3
> ```

---

## 1.7 Generate `requirements.txt`

```bash
pip freeze > requirements.txt
```

This creates a file listing all installed packages with their exact versions:

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

## 1.8 Verify — Run the Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

Open `http://127.0.0.1:8000/` in your browser. You should see the Django welcome rocket! 🚀

Press `Ctrl+C` to stop.

---

## ✅ What You've Built

At this point you have:
- ✅ A virtual environment with all packages installed
- ✅ A Django project (`ProjectManagerCore`)
- ✅ Two empty apps (`auth_handler`, `project_handler`)
- ✅ A `.env` file with your MongoDB connection string and secret key
- ✅ A `requirements.txt` file others can use to install your dependencies

**Next step:** Configure `settings.py` to wire everything together.

---

## 🔗 Navigation

← **[Back to My Django Project](../my_django_project.md)**

→ **Next: [Step 2 — Settings & Configuration](./my_project_settings.md)**
