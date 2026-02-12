# 📚 ProjectManager — Backend Documentation

Welcome! This repository contains a **Django REST Framework** backend that uses **MongoDB** and **JWT authentication** to manage Projects and Tasks.

This documentation is structured so you can either **learn Django from scratch** or **understand how this specific project was built** step by step.

---

## 📖 Table of Contents

### 1. 🎓 [Learning Django & DRF](./DocumentationBackend/learning_django.md)

> **Start here if you're new to Django.**
>
> Covers the fundamentals — virtual environments, project setup, file structure, models, views, URLs, serializers, REST Framework, MongoDB fields, JWT, and how to manage dependencies.

---

### 2. 🛠️ [My Django Project — Step by Step](./DocumentationBackend/my_django_project.md)

> **Start here if you want to recreate this project.**
>
> A "build with me" walkthrough — from scaffolding the project skeleton, to configuring settings, to writing the auth module, to building the full CRUD project/task system. Every file explained, every code snippet included.

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Clone and enter the project
git clone <repo_url>
cd "ProjectManager Backend"

# 2. Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate          # Windows
# source venv/bin/activate       # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (same level as manage.py)
# CONNECTION_STRING=mongodb+srv://<user>:<pass>@cluster.mongodb.net/
# SECRET_KEY=your-secret-key

# 5. Run the server
python manage.py runserver
```

> 📖 For the full setup guide, see **[My Project → Scaffolding](./DocumentationBackend/my_project/my_project_scaffolding.md)**
