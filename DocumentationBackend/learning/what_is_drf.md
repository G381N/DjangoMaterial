# 🔌 What is Django REST Framework (DRF)?

## The Problem

Django by itself is designed to serve **HTML pages** (templates). But modern apps need a **JSON API** that a frontend (React, Vue, mobile app) can call.

You *could* build an API with plain Django using `JsonResponse`, but you'd have to manually handle:
- Request parsing (JSON body)
- Response formatting
- Authentication
- Permissions
- Validation
- Pagination

**Django REST Framework (DRF)** handles all of that for you.

---

## What DRF Adds

| Feature | Plain Django | With DRF |
|---------|-------------|----------|
| Parse JSON body | `json.loads(request.body)` | `request.data` (automatic) |
| Return JSON | `JsonResponse({...})` | `Response({...})` (automatic) |
| Authentication | Build it yourself | Built-in (Token, JWT, Session) |
| Permissions | Build it yourself | `IsAuthenticated`, `AllowAny`, custom |
| Serialization | Manual dict building | `Serializer` classes |
| Pagination | Build it yourself | `PageNumberPagination` |
| Browsable API | ❌ | ✅ (free debug UI in browser) |

---

## Installation

```bash
pip install djangorestframework
```

Then add to `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

---

## Key Concepts

### 1. `APIView` — Class-Based Views

DRF's version of Django's `View`. Each HTTP method gets its own method:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.data.get("name")
        return Response({"message": f"Hello, {name}!"}, status=status.HTTP_201_CREATED)
```

---

### 2. `Response` — Smart JSON Responses

```python
from rest_framework.response import Response

# DRF automatically converts Python dicts to JSON
return Response({"key": "value"}, status=200)
```

You don't need `json.dumps()` or `JsonResponse` — DRF handles it.

---

### 3. `request.data` — Parsed Request Body

```python
# DRF automatically parses the JSON body:
data = request.data        # Already a Python dict
name = data.get("name")   # Access fields directly
```

No need for `json.loads(request.body)`.

---

### 4. Permissions — Who Can Access?

```python
from rest_framework.permissions import IsAuthenticated, AllowAny

class PublicView(APIView):
    permission_classes = (AllowAny,)         # Anyone can access
    ...

class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)  # Must be logged in
    ...
```

You can set a **global default** in `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Secure by default
    ),
}
```

Then only override with `AllowAny` on specific views (like login/register).

---

### 5. `request.user` — The Authenticated User

When a user is authenticated (via JWT), DRF automatically sets `request.user`:

```python
class MyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user                # The logged-in user object
        return Response({"username": user.username})
```

> This is populated by the authentication backend (in our case, `MongoJWTAuthentication` in `backends.py`).

---

### 6. Status Codes

DRF provides readable constants:

```python
from rest_framework import status

status.HTTP_200_OK           # 200
status.HTTP_201_CREATED      # 201
status.HTTP_204_NO_CONTENT   # 204
status.HTTP_400_BAD_REQUEST  # 400
status.HTTP_401_UNAUTHORIZED # 401
status.HTTP_403_FORBIDDEN    # 403
status.HTTP_404_NOT_FOUND    # 404
```

---

## DRF in `settings.py`

This is how we configure DRF globally:

```python
REST_FRAMEWORK = {
    # Use our custom MongoDB JWT backend for authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth_handler.backends.MongoJWTAuthentication',
    ),
    # Require login by default on all endpoints
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Paginate list responses
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

---

## 🔗 Navigation

← **[Previous: Models, Views & URLs](./models_views_urls.md)**

← **[Back to Learning Django](../learning_django.md)**

→ **Next: [Serializers Explained](./serializers_explained.md)**
