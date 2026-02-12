# 🗄️ Step 3: Database Connection (`db.py`)

This step covers creating the `db.py` file inside `ProjectManagerCore/` — the file that connects your Django app to MongoDB Atlas.

> **By the end of this step, you'll have:** A working MongoDB connection with two separate database aliases for logical separation of data.

---

## Why Do We Need `db.py`?

Django's built-in database system (`DATABASES` in settings.py) is designed for **SQL databases** (PostgreSQL, SQLite, MySQL).

We're using **MongoDB** through **MongoEngine**, which is a completely separate system. MongoEngine needs to be manually connected when the app starts up — it doesn't use Django's `DATABASES` config at all.

We created a separate `db.py` file to keep this logic clean and separate from `settings.py`.

---

## 3.1 Create the File

Create `ProjectManagerCore/db.py`:

```python
from pathlib import Path
import os
from dotenv import load_dotenv
from mongoengine import connect

# Optional: mongomock for testing without a real MongoDB
try:
    import mongomock
except Exception:
    mongomock = None

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Get MongoDB connection string from environment
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
if not CONNECTION_STRING:
    if not mongomock:
        raise Exception(
            "The Connection String is not set in the .env file "
            "and mongomock is not installed. "
            "Set CONNECTION_STRING or install mongomock."
        )
```

---

## 3.2 The `init_db()` Function

```python
def init_db():
    if CONNECTION_STRING:
        # Production: connect to real MongoDB Atlas
        connect(db="project_manager_auth", alias="auth_db", host=CONNECTION_STRING)
        connect(db="project_manager", alias="project_db", host=CONNECTION_STRING)
    else:
        # Testing/Dev: use in-memory mock
        connect(db="project_manager_auth", alias="auth_db",
                host="mongodb://localhost", mongo_client_class=mongomock.MongoClient)
        connect(db="project_manager", alias="project_db",
                host="mongodb://localhost", mongo_client_class=mongomock.MongoClient)
```

---

## 3.3 Understanding the Arguments

```python
connect(
    db="project_manager_auth",    # Database name in MongoDB
    alias="auth_db",              # Name we use in our code to refer to this connection
    host=CONNECTION_STRING         # Full MongoDB Atlas connection string
)
```

| Argument | What it means |
|----------|--------------|
| `db` | The name of the database within MongoDB. MongoDB auto-creates it if it doesn't exist |
| `alias` | A label we use in our model's `meta` to say "store this in this database" |
| `host` | The MongoDB connection string (from `.env`) |

---

## 3.4 Why Two Databases?

We create two separate connections:

| Alias | Database Name | Stores |
|-------|--------------|--------|
| `auth_db` | `project_manager_auth` | User documents |
| `project_db` | `project_manager` | Project and Task documents |

In MongoDB Atlas, that looks like:

```
MongoDB Cluster
├── project_manager_auth    ← auth_db alias
│   └── users collection
│
└── project_manager         ← project_db alias
    ├── projects collection
    └── tasks collection
```

**Why separate?** Logical separation — authentication data stays separate from business data. Both use the same cluster (same `CONNECTION_STRING`), so there's no performance cost.

**How models reference it:**
```python
# In auth_handler/models.py:
class User(Document):
    meta = {"collection": "users", "db_alias": "auth_db"}   # ← Uses the auth_db alias

# In project_handler/models.py:
class Project(Document):
    meta = {"collection": "projects", "db_alias": "project_db"}  # ← Uses the project_db alias
```

---

## 3.5 The `mongomock` Fallback

```python
try:
    import mongomock
except Exception:
    mongomock = None
```

**What is `mongomock`?** An in-memory MongoDB clone for testing. When you run `python manage.py test`, you don't want to hit your real database. `mongomock` creates a fake MongoDB in memory that behaves the same way.

If `CONNECTION_STRING` is not set **and** `mongomock` is installed → use the mock.
If `CONNECTION_STRING` is not set **and** `mongomock` is NOT installed → raise an error.

---

## 3.6 How It's Called

In `settings.py` (at the bottom):

```python
try:
    from .db import init_db
    init_db()
except Exception:
    pass
```

- `from .db import init_db` — imports `init_db` from the `db.py` file in the same folder (`.` means current package)
- `init_db()` — runs the function, establishing both MongoDB connections
- `try/except` — catches errors gracefully so Django doesn't crash if MongoDB is unreachable

> This runs **once** when Django starts up. After that, MongoEngine uses the established connections automatically whenever you query a model.

---

## ✅ Complete `db.py`

<details>
<summary>Click to expand the full file</summary>

```python
from pathlib import Path
import os
from dotenv import load_dotenv
from mongoengine import connect

# Optional mongomock fallback for tests/local dev when no real Mongo is available
try:
    import mongomock
except Exception:
    mongomock = None

# Loading environment variables from the project .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Getting the MongoDB connection string from .env
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
if not CONNECTION_STRING:
    if not mongomock:
        raise Exception(
            "The Connection String is not set in the .env file "
            "and mongomock is not installed. "
            "Set CONNECTION_STRING or install mongomock."
        )

def init_db():
    # Connect auth DB (alias: auth_db)
    if CONNECTION_STRING:
        connect(db="project_manager_auth", alias="auth_db", host=CONNECTION_STRING)
        connect(db="project_manager", alias="project_db", host=CONNECTION_STRING)
    else:
        # Use mongomock for in-memory testing/dev
        connect(db="project_manager_auth", alias="auth_db",
                host="mongodb://localhost", mongo_client_class=mongomock.MongoClient)
        connect(db="project_manager", alias="project_db",
                host="mongodb://localhost", mongo_client_class=mongomock.MongoClient)
```

</details>

---

## 🔗 Navigation

← **[Previous: Step 2 — Settings & Configuration](./my_project_settings.md)**

← **[Back to My Django Project](../my_django_project.md)**

→ **Next: [Step 4 — Auth Module](./steps_auth_module.md)**
