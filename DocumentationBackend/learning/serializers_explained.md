# 🔄 Serializers Explained

## What is a Serializer?

A serializer does two things:

1. **Serialization** — Converts a Python object (like a MongoEngine document) into JSON-friendly data (for API responses)
2. **Deserialization** — Converts incoming JSON data into validated Python data (for creating/updating objects)

**Think of it as a translator** between your database objects and JSON.

---

## Why Not Just Use Dicts?

You *could* manually build dicts:
```python
# Without serializer (manual, error-prone)
return Response({
    "id": str(user.id),
    "username": user.username,
    "email": user.email,
    # Oops, what if you accidentally include the password?
})
```

With a serializer, you **declare once** which fields to include, which are read-only, and how to validate — clean and reusable.

---

## Basic Serializer Example

```python
from rest_framework_mongoengine.serializers import DocumentSerializer
from auth_handler.models import User

class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "created_at")
```

**What this does:**
- Only exposes `id`, `username`, `email`, `created_at` — **password is excluded**
- Automatically converts MongoEngine field types to JSON-safe types
- `DocumentSerializer` is the MongoEngine version of DRF's `ModelSerializer`

### Using it in a view:
```python
user = User.objects(email="john@email.com").first()
data = UserSerializer(user).data
# data = {"id": "abc123", "username": "john", "email": "john@email.com", "created_at": "..."}
```

### Serializing multiple objects:
```python
users = User.objects.all()
data = UserSerializer(users, many=True).data
# data = [{"id": "...", ...}, {"id": "...", ...}]
```

---

## Serializer with Validation

```python
class RegisterSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "created_at")
        read_only_fields = ("id", "created_at")
        extra_kwargs = {"password": {"write_only": True}}
```

### Understanding the Meta options:

| Option | What it does |
|--------|-------------|
| `model` | Which MongoEngine document this serializer is for |
| `fields` | Which fields to include (whitelist) |
| `read_only_fields` | Fields that appear in responses but can't be set by the client |
| `extra_kwargs` | Additional settings per field |
| `write_only: True` | Field can be sent in request but won't appear in response (perfect for passwords) |

---

## Field-Level Validation

You can add `validate_<fieldname>()` methods to validate individual fields:

```python
class RegisterSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "created_at")
        read_only_fields = ("id", "created_at")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        """Check if email is already taken."""
        if User.objects(email=value).first():
            raise ValidationError("This email is already registered")
        return value

    def validate_username(self, value):
        """Check if username is already taken."""
        if User.objects(username=value).first():
            raise ValidationError("This username is already taken")
        return value
```

**How it works:**
- DRF automatically calls `validate_<fieldname>()` for each field during `is_valid()`
- If validation fails, it raises `ValidationError` → DRF returns HTTP 400 with the error message
- If validation passes, return the (possibly cleaned) value

---

## Object-Level Validation

The `validate()` method runs after all field-level validators:

```python
def validate(self, attrs):
    """Cross-field validation: check passwords match."""
    pw = attrs.get("password")
    pwc = self.initial_data.get("password_confirm")
    if not pw or pw != pwc:
        raise ValidationError("Passwords do not match")
    return attrs
```

> `self.initial_data` — The raw request data (before parsing). Useful for accessing fields that aren't in the serializer's `fields` (like `password_confirm`).

---

## The `create()` Method

Override `create()` to control how the object is saved:

```python
def create(self, validated_data):
    # Remove password_confirm if present (it's not a model field)
    validated_data.pop("password_confirm", None)

    # Extract password to hash it separately
    raw_password = validated_data.pop("password", None)

    # Create user with remaining fields
    user = User(**validated_data)

    # Hash the password
    if raw_password:
        user.set_password(raw_password)

    user.save()
    return user
```

---

## The Full Call Flow in a View

```python
# In views.py:
serializer = RegisterSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
# ↑ This calls:
#   1. validate_email(value)   → field-level
#   2. validate_username(value) → field-level
#   3. validate(attrs)          → object-level

user = serializer.save()
# ↑ This calls:
#   4. create(validated_data)   → saves to DB
```

---

## Read-Only Example (Response Serializer)

Sometimes you want a serializer just for formatting responses:

```python
class ProjectSerializer(DocumentSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "description", "owner", "created_at")
        read_only_fields = ("id", "owner", "created_at")
```

The `owner` is read-only because it's set in the view (`project.owner = request.user`), not from the client's request body.

---

## 🔗 Navigation

← **[Previous: What is DRF?](./what_is_drf.md)**

← **[Back to Learning Django](../learning_django.md)**

→ **Next: [MongoEngine Field Types](./mongoengine_fields.md)**
