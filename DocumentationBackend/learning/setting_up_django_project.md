# 🚀 Setting Up Your First Django Project

This guide walks you through creating a brand new Django project from an empty folder to a running development server.

---

## Step 1: Create a Project Folder

```bash
mkdir MyProject
cd MyProject
```

---

## Step 2: Set Up a Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate       # Windows
# source venv/bin/activate    # Mac/Linux
```

You should see `(venv)` in your terminal prompt.

> 📖 See **[Virtual Environments](./virtual_environments.md)** for a detailed explanation.

---

## Step 3: Install Django

```bash
pip install django
```

Verify it installed:
```bash
python -m django --version
# Output: 6.0.2 (or whatever version)
```

---

## Step 4: Create the Django Project

```bash
django-admin startproject ProjectManagerCore .
```

**Breaking this down:**
- `django-admin` — Django's command-line admin tool
- `startproject` — Creates a new Django project
- `ProjectManagerCore` — The name of your project (this becomes the settings folder)
- `.` — **Important!** The dot means "create it in the current directory" (without the dot, Django creates a nested folder)

**After running this, your folder looks like:**
```
MyProject/
├── manage.py
└── ProjectManagerCore/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

---

## Step 5: Test the Server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. You should see the Django welcome rocket page! 🚀

Press `Ctrl+C` to stop the server.

---

## Step 6: Create an App

Django projects are organized into **apps**. An app is a module that handles one specific feature.

```bash
python manage.py startapp auth_handler
```

This creates:
```
auth_handler/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── views.py
└── migrations/
    └── __init__.py
```

> **Note:** You can create as many apps as you want. For example:
> ```bash
> python manage.py startapp project_handler
> ```

---

## Step 7: Register the App

Django doesn't know about your new app until you register it. Open `ProjectManagerCore/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps (add these lines)
    'auth_handler',
    'project_handler',
]
```

---

## Step 8: Save Your Dependencies

```bash
pip freeze > requirements.txt
```

> 📖 See **[Requirements & Dependencies](./requirements_and_dependencies.md)** for more details.

---

## Summary of Commands

| Command | What it does |
|---------|-------------|
| `python -m venv venv` | Create a virtual environment |
| `.\venv\Scripts\activate` | Activate the virtual environment (Windows) |
| `pip install django` | Install Django |
| `django-admin startproject <name> .` | Create a new Django project |
| `python manage.py startapp <name>` | Create a new app inside the project |
| `python manage.py runserver` | Start the development server |
| `pip freeze > requirements.txt` | Save installed packages to a file |

---

## What's Next?

Now that you have a project running, learn about what each file does:

→ **[Django File Structure](./django_file_structure.md)**

---

## 🔗 Navigation

← **[Previous: Requirements & Dependencies](./requirements_and_dependencies.md)**

← **[Back to Learning Django](../learning_django.md)**
