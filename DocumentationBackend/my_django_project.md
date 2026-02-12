# 🛠️ My Django Project — Step by Step

## What is This Project?

**ProjectManager** is a REST API backend that lets users:
- **Register** and **Login** (with JWT authentication)
- **Create**, **Read**, **Update**, and **Delete** their own **Projects**
- Add **Tasks** to their projects with status tracking (`Todo`, `In Progress`, `Done`)

It's built with ownership-based security — every user can only see and manage their own data.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Django 6.0** | Web framework |
| **Django REST Framework** | REST API layer |
| **MongoEngine** | MongoDB ODM |
| **django-rest-framework-mongoengine** | DRF ↔ MongoEngine bridge |
| **djangorestframework-simplejwt** | JWT auth tokens |
| **MongoDB Atlas** | Cloud database |
| **Werkzeug** | Password hashing |
| **python-dotenv** | Environment variables (`.env`) |
| **django-cors-headers** | Frontend CORS support |
| **mongomock** | In-memory MongoDB for testing |

---

## Two Apps

| App | Responsibility | Database |
|-----|---------------|----------|
| `auth_handler` | User registration, login, JWT generation, custom JWT backend | `project_manager_auth` (alias: `auth_db`) |
| `project_handler` | CRUD for Projects and Tasks, ownership checks, status filtering | `project_manager` (alias: `project_db`) |

---

## My `requirements.txt`

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

> 📖 See **[Requirements & Dependencies](./learning/requirements_and_dependencies.md)** for what each package does.

---

## 📖 Build With Me — Step by Step

Follow these steps **in order** to recreate this entire project from scratch. Each step is its own document with full code snippets you can copy.

| Step | Topic | What You'll Build |
|------|-------|-------------------|
| **1** | 🏗️ **[Scaffolding the Project](./my_project/my_project_scaffolding.md)** | Virtual environment, installing packages, `startproject`, `startapp`, `.env`, `requirements.txt` |
| **2** | ⚙️ **[Settings & Configuration](./my_project/my_project_settings.md)** | `settings.py` — installed apps, DRF config, JWT config, CORS, middleware |
| **3** | 🗄️ **[Database Connection](./my_project/my_project_db.md)** | `db.py` — connecting to MongoDB Atlas with two database aliases |
| **4** | 🔐 **[Auth Module](./my_project/steps_auth_module.md)** | `auth_handler` — User model, serializers, register/login views, custom JWT backend, URLs |
| **5** | 📂 **[Project Module](./my_project/steps_project_module.md)** | `project_handler` — Project & Task models, serializers, CRUD views with ownership, URLs |

---

## 🔗 Navigation

← **[Back to Main README](../README.md)**

← **[Learning Django & DRF](./learning_django.md)**
