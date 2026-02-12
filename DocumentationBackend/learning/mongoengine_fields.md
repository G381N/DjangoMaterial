# 🍃 MongoEngine Field Types

MongoEngine is an **ODM (Object Document Mapper)** for MongoDB — similar to how Django's ORM works for SQL databases, but for MongoDB documents.

> **ODM vs ORM:**
> - **ORM** (Object Relational Mapper) — Maps Python objects to SQL tables
> - **ODM** (Object Document Mapper) — Maps Python objects to MongoDB documents (JSON-like)

---

## Commonly Used Fields

### `StringField`
Stores text. The most common field.

```python
from mongoengine import Document, StringField

class User(Document):
    username = StringField(required=True, unique=True)
    bio = StringField(max_length=500)
```

| Option | Description |
|--------|-------------|
| `required=True` | Must be provided, can't be empty |
| `unique=True` | No two documents can have the same value |
| `max_length=500` | Maximum number of characters |
| `default="Hello"` | Default value if not provided |
| `choices=("A", "B", "C")` | Only these values are allowed |

---

### `EmailField`
Like `StringField` but validates email format.

```python
email = EmailField(required=True, unique=True)
```

---

### `IntField`
Stores integers.

```python
age = IntField(min_value=0, max_value=150)
```

---

### `FloatField`
Stores decimal numbers.

```python
price = FloatField(min_value=0.0)
```

---

### `BooleanField`
Stores `True` or `False`.

```python
is_active = BooleanField(default=True)
```

---

### `DateTimeField`
Stores date and time.

```python
from datetime import datetime

created_at = DateTimeField(default=datetime.utcnow)
```

> ⚠️ Note: Pass `datetime.utcnow` (without `()`). With `()`, it would set the same timestamp for all documents (evaluated once at class definition). Without `()`, it's called fresh for each new document.

---

### `ReferenceField`
Links to another document — like a **foreign key** in SQL.

```python
from mongoengine import ReferenceField

class Project(Document):
    name = StringField(required=True)
    owner = ReferenceField('auth_handler.models.User', required=True)
```

**What it stores:** The `ObjectId` of the referenced document.

**How to use it:**
```python
project = Project.objects.filter(id=project_id).first()
print(project.owner.username)  # MongoEngine auto-fetches the referenced User
```

> You can pass either a string path (`'auth_handler.models.User'`) or the class itself if it's in the same file.

---

### `ListField`
Stores a list of items.

```python
tags = ListField(StringField(), default=list)
```

---

### `DictField`
Stores a dictionary (key-value pairs).

```python
metadata = DictField()
```

---

### `ObjectIdField`
Stores a MongoDB ObjectId. Every document automatically gets an `id` field of this type.

---

## Field Options Reference

These options work on **all field types**:

| Option | Type | Description |
|--------|------|-------------|
| `required` | `bool` | If `True`, the field must be provided |
| `default` | `any` | Value to use if the field isn't provided |
| `unique` | `bool` | If `True`, enforces uniqueness across all documents |
| `choices` | `tuple` | Restricts the field to only these values |
| `null` | `bool` | If `True`, allows `null` values |
| `db_field` | `str` | The actual field name in MongoDB (if different from Python name) |
| `primary_key` | `bool` | If `True`, this field is used as the document's `_id` |

---

## The `meta` Dictionary

Every document class has a `meta` dict for configuration:

```python
class User(Document):
    meta = {
        "collection": "users",         # MongoDB collection name
        "db_alias": "auth_db",          # Which database connection to use
    }
```

| Key | Description |
|-----|-------------|
| `collection` | The name of the MongoDB collection (default: class name in lowercase) |
| `db_alias` | The MongoEngine connection alias to use (defined in `db.py`) |
| `ordering` | Default sort order, e.g., `["-created_at"]` (newest first) |
| `indexes` | Custom indexes for query performance |

---

## Document vs EmbeddedDocument

### `Document` — Top-level (gets its own collection)
```python
class Project(Document):
    name = StringField()
```

### `EmbeddedDocument` — Nested inside another document (no own collection)
```python
class Address(EmbeddedDocument):
    street = StringField()
    city = StringField()

class User(Document):
    name = StringField()
    address = EmbeddedDocumentField(Address)
```

**In MongoDB, this stores:**
```json
{
    "name": "John",
    "address": {
        "street": "123 Main St",
        "city": "New York"
    }
}
```

---

## Common Queries

```python
# Get all documents
users = User.objects.all()

# Get first match
user = User.objects(email="john@email.com").first()

# Filter
projects = Project.objects.filter(owner=user)

# Filter with choices
tasks = Task.objects.filter(status="Done")

# Count
count = Task.objects.filter(project=project).count()

# Order by
projects = Project.objects.filter(owner=user).order_by("-created_at")

# Delete
user.delete()
```

---

## Fields Used in This Project

| Model | Field | Type | Notes |
|-------|-------|------|-------|
| `User` | `username` | `StringField` | required, unique |
| `User` | `email` | `EmailField` | required, unique |
| `User` | `password` | `StringField` | required, hashed |
| `User` | `created_at` | `DateTimeField` | default=utcnow |
| `Project` | `name` | `StringField` | required |
| `Project` | `description` | `StringField` | optional |
| `Project` | `owner` | `ReferenceField` | → User |
| `Project` | `created_at` | `DateTimeField` | default=utcnow |
| `Task` | `title` | `StringField` | required |
| `Task` | `description` | `StringField` | optional |
| `Task` | `status` | `StringField` | choices: Todo, In Progress, Done |
| `Task` | `project` | `ReferenceField` | → Project |
| `Task` | `created_at` | `DateTimeField` | default=utcnow |

---

## 🔗 Navigation

← **[Previous: Serializers Explained](./serializers_explained.md)**

← **[Back to Learning Django](../learning_django.md)**

→ **Next: [JWT Authentication](./jwt_explained.md)**
