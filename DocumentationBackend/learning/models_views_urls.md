# 🧩 Models, Views & URLs — The Core Pattern

This is **the most important concept in Django**. Everything revolves around three files: `models.py`, `views.py`, and `urls.py`. Understanding how they connect is the key to understanding Django.

---

## The Big Picture

```
Client sends request
       │
       ▼
   urls.py          ← "Which view handles this URL?"
       │
       ▼
   views.py         ← "What logic should run?" (business logic)
       │
       ▼
   models.py        ← "What data do I need?" (database interaction)
       │
       ▼
   Response (JSON)  ← Sent back to the client
```

---

## 1. Models (`models.py`) — The Data Layer

**What it defines:** The structure of your data — what fields exist, their types, and their constraints.

**Think of it as:** A blueprint for a MongoDB document (or SQL table if using Django's ORM).

### Example (MongoEngine):
```python
from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime

class User(Document):
    meta = {"collection": "users", "db_alias": "auth_db"}

    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)
```

**Key points:**
- Each class = one MongoDB collection (or SQL table)
- Fields define what data is stored
- Methods add behavior (like password hashing)
- `meta` tells MongoEngine which database and collection to use

### Common Operations:
```python
# Create and save
user = User(username="john", email="john@email.com")
user.save()

# Query
user = User.objects(email="john@email.com").first()

# Filter
all_users = User.objects.filter(username="john")

# Delete
user.delete()
```

---

## 2. Views (`views.py`) — The Logic Layer

**What it defines:** What happens when a specific API endpoint is hit — validation, business logic, database queries, and responses.

**Think of it as:** The brain — it receives a request, processes it, and returns a response.

### Example (DRF Class-Based View):
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)     # No auth needed for registration

    def post(self, request):
        data = request.data              # Get the JSON body

        # 1. Validate
        if not data.get("username"):
            return Response(
                {"detail": "Username is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Create
        user = User(username=data["username"], email=data["email"])
        user.set_password(data["password"])
        user.save()

        # 3. Respond
        return Response(
            {"message": "User created!", "user": {"id": str(user.id)}},
            status=status.HTTP_201_CREATED
        )
```

**Key points:**
- Each class = one endpoint (or group of related endpoints)
- HTTP methods map to class methods: `get()`, `post()`, `put()`, `delete()`
- `request.data` gives you the JSON body
- `request.user` gives you the authenticated user (set by the JWT backend)
- Always return a `Response()` with a status code

### Common Status Codes:
```python
status.HTTP_200_OK           # Success
status.HTTP_201_CREATED      # Successfully created
status.HTTP_204_NO_CONTENT   # Deleted successfully (no body)
status.HTTP_400_BAD_REQUEST  # Client sent bad data
status.HTTP_401_UNAUTHORIZED # Not logged in / bad credentials
status.HTTP_403_FORBIDDEN    # Logged in but not allowed
status.HTTP_404_NOT_FOUND    # Resource doesn't exist
```

---

## 3. URLs (`urls.py`) — The Routing Layer

**What it defines:** Which URL pattern maps to which View.

**Think of it as:** A phone directory — "If someone calls this number, connect them to this person."

### App-level `urls.py` (e.g., `auth_handler/urls.py`):
```python
from django.urls import path
from auth_handler.views import RegisterAPIView, LoginAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="auth-register"),
    path("login/", LoginAPIView.as_view(), name="auth-login"),
]
```

### Project-level `urls.py` (e.g., `ProjectManagerCore/urls.py`):
```python
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('auth_handler.urls')),       # Forwards to auth app
    path('api/projects/', include('project_handler.urls')), # Forwards to project app
]
```

**How the routing chain works:**

```
Request: POST /api/auth/register/
                │
                ▼
ProjectManagerCore/urls.py
    path('api/auth/', include('auth_handler.urls'))
    Matches 'api/auth/' → forwards 'register/' to auth_handler
                │
                ▼
auth_handler/urls.py
    path("register/", RegisterAPIView.as_view())
    Matches 'register/' → calls RegisterAPIView.post()
                │
                ▼
RegisterAPIView.post(request) runs
```

**Key points:**
- `path("register/", ...)` — Maps a URL pattern to a view
- `.as_view()` — Converts a class-based view into a callable
- `include('app.urls')` — Delegates URL matching to another app's urls.py
- `name="auth-register"` — A label you can use in tests: `reverse('auth-register')`

---

## How They All Connect — Full Example

Let's trace a **Login** request through all three layers:

### 1. `urls.py` — Route the request
```python
# ProjectManagerCore/urls.py
path('api/auth/', include('auth_handler.urls'))

# auth_handler/urls.py
path("login/", LoginAPIView.as_view(), name="auth-login")
```

### 2. `views.py` — Handle the logic
```python
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        credential = request.data.get("first_credential")
        password = request.data.get("password")

        # Query the model
        user = User.objects(email=credential).first()
        if not user:
            user = User.objects(username=credential).first()

        if not user or not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
```

### 3. `models.py` — Define the data
```python
class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)
```

---

## 🔗 Navigation

← **[Previous: Django File Structure](./django_file_structure.md)**

← **[Back to Learning Django](../learning_django.md)**

→ **Next: [What is Django REST Framework?](./what_is_drf.md)**
