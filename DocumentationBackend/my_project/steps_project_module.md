# 📂 Step 5: Project Module (`project_handler`)

Build the full CRUD system for Projects and Tasks — models, serializers, views with ownership checks, status filtering, and URL routing.

> **By the end of this step:** Full REST API for creating, reading, updating, and deleting Projects and Tasks with ownership-based security.

---

## Files We'll Create

| File | Purpose |
|------|---------|
| `models.py` | Project and Task documents |
| `serializers.py` | Validation and data shaping |
| `views.py` | CRUD endpoints with ownership checks |
| `urls.py` | URL routing |

---

## 5.1 Models (`models.py`)

> 📖 Prereq: [MongoEngine Fields](../learning/mongoengine_fields.md)

```python
from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime

class Project(Document):
    meta = {"collection": "projects", "db_alias": "project_db"}

    name = StringField(required=True)
    description = StringField()
    owner = ReferenceField('auth_handler.models.User', required=True)
    created_at = DateTimeField(default=datetime.utcnow)


class Task(Document):
    meta = {"collection": "tasks", "db_alias": "project_db"}

    title = StringField(required=True)
    description = StringField()
    status = StringField(choices=("Todo", "In Progress", "Done"), default="Todo")
    project = ReferenceField(Project, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
```

**Key concepts:**
- Both use `db_alias: "project_db"` → stored in the `project_manager` database
- `ReferenceField` → Like a foreign key. `owner` links Project → User, `project` links Task → Project
- `choices=("Todo", "In Progress", "Done")` → Only these values are allowed for status
- `default="Todo"` → New tasks start as "Todo" if no status is provided

---

## 5.2 Serializers (`serializers.py`)

> 📖 Prereq: [Serializers Explained](../learning/serializers_explained.md)

```python
from rest_framework_mongoengine.serializers import DocumentSerializer
from project_handler.models import Project, Task
from rest_framework.exceptions import ValidationError

class ProjectSerializer(DocumentSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "description", "owner", "created_at")
        read_only_fields = ("id", "owner", "created_at")


class TaskSerializer(DocumentSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "project", "created_at")
        read_only_fields = ("id", "project", "created_at")

    def validate_status(self, value):
        allowed = ("Todo", "In Progress", "Done")
        if value not in allowed:
            raise ValidationError(f"Invalid status. Choose from {allowed}")
        return value
```

**Why `read_only`?**
- `owner` → Auto-set from `request.user` in the view (prevents users from setting owner to someone else)
- `project` → Auto-set from the URL's project_id (prevents cross-project assignment)
- `created_at` → Auto-set by the model default

---

## 5.3 Views (`views.py`)

> 📖 Prereq: [What is DRF?](../learning/what_is_drf.md)

### Helper + Imports

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from project_handler.models import Project, Task
from project_handler.serializers import ProjectSerializer, TaskSerializer

def validate_keys(data, required_keys):
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return Response(
            {"message": "There is a Missing Field ...", "missing_fields": missing_keys},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None
```

### ProjectListCreateAPIView — List & Create Projects

```python
class ProjectListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """List all projects owned by the logged-in user."""
        user = request.user
        projects_under_user = Project.objects.filter(owner=user)
        data = ProjectSerializer(projects_under_user, many=True).data
        return Response({"results": data}, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new project (owner = current user)."""
        data = request.data or {}
        name = data.get("name")
        description = data.get("description")

        req = ("name",)
        missing = validate_keys(data, req)
        if missing:
            return missing

        user = request.user
        project = Project()
        try:
            project.name = name
            if description:
                project.description = description
            project.owner = user
            project.save()
        except Exception:
            return Response({"detail": "Failed to create project ..."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "project": ProjectSerializer(project).data,
            "message": "Project Created Successfully ..."
        }, status=status.HTTP_201_CREATED)
```

**Security:** `GET` filters by `owner=request.user` → users only see their own projects.

### ProjectDetailAPIView — Get, Update & Delete a Project

```python
class ProjectDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, project_id):
        return Project.objects.filter(id=project_id).first()

    def get(self, request, project_id):
        project = self.get_object(project_id)
        if not project:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        if project.owner != request.user:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return Response(ProjectSerializer(project).data, status=status.HTTP_200_OK)

    def put(self, request, project_id):
        project = self.get_object(project_id)
        if not project:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        if project.owner != request.user:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        raw = request.data or {}
        name = raw.get("name")
        description = raw.get("description")
        if name:
            project.name = name
        if description is not None:
            project.description = description
        project.save()
        return Response(ProjectSerializer(project).data, status=status.HTTP_200_OK)

    def delete(self, request, project_id):
        project = self.get_object(project_id)
        if not project:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        if project.owner != request.user:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**Security pattern (every method):**
1. Find the project → 404 if not found
2. Check `project.owner != request.user` → 403 if you don't own it
3. Proceed with the operation

### TaskListCreateAPIView — List & Create Tasks

```python
class TaskListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, project_id):
        """List tasks for a project. Supports ?status= filter."""
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        if project.owner != request.user:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        status_filter = request.query_params.get("status")
        tasks_in_project = Task.objects.filter(project=project)
        if status_filter:
            tasks_in_project = tasks_in_project.filter(status=status_filter)

        data = TaskSerializer(tasks_in_project, many=True).data
        return Response({"results": data}, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        """Create a task under a project."""
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        if project.owner != request.user:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        raw = request.data or {}
        req = ("title",)
        missing = validate_keys(raw, req)
        if missing:
            return missing

        title = raw.get("title")
        description = raw.get("description")
        status_val = raw.get("status") or "Todo"

        task = Task()
        try:
            task.title = title
            if description:
                task.description = description
            task.status = status_val
            task.project = project
            task.save()
        except Exception:
            return Response({"detail": "Failed to create task"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "task": TaskSerializer(task).data,
            "message": "Task Created Successfully ..."
        }, status=status.HTTP_201_CREATED)
```

**Status filtering:** `GET /api/projects/<id>/tasks/?status=Done` returns only completed tasks.

### TaskDetailAPIView — Update & Delete a Task

```python
class TaskDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, task_id):
        return Task.objects.filter(id=task_id).first()

    def put(self, request, task_id):
        task = self.get_object(task_id)
        if not task:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        if task.project.owner != request.user:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        raw = request.data or {}
        if raw.get("title"):
            task.title = raw["title"]
        if raw.get("description") is not None:
            task.description = raw["description"]
        if raw.get("status"):
            task.status = raw["status"]
        task.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    def delete(self, request, task_id):
        task = self.get_object(task_id)
        if not task:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        if task.project.owner != request.user:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**Task ownership:** `task.project.owner` — ownership is checked through the parent project, not on the task itself.

---

## 5.4 URLs (`urls.py`)

```python
from django.urls import path
from project_handler.views import (
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
    TaskListCreateAPIView,
    TaskDetailAPIView,
)

urlpatterns = [
    path("", ProjectListCreateAPIView.as_view(), name="project-list-create"),
    path("<str:project_id>/", ProjectDetailAPIView.as_view(), name="project-detail"),
    path("<str:project_id>/tasks/", TaskListCreateAPIView.as_view(), name="task-list-create"),
    path("tasks/<str:task_id>/", TaskDetailAPIView.as_view(), name="task-detail"),
]
```

### Full URL Map (with `/api/projects/` prefix from core router):

| Full URL | Method | View | Description |
|----------|--------|------|-------------|
| `/api/projects/` | GET | `ProjectListCreateAPIView` | List my projects |
| `/api/projects/` | POST | `ProjectListCreateAPIView` | Create project |
| `/api/projects/<id>/` | GET | `ProjectDetailAPIView` | Get project |
| `/api/projects/<id>/` | PUT | `ProjectDetailAPIView` | Update project |
| `/api/projects/<id>/` | DELETE | `ProjectDetailAPIView` | Delete project |
| `/api/projects/<id>/tasks/` | GET | `TaskListCreateAPIView` | List tasks |
| `/api/projects/<id>/tasks/` | POST | `TaskListCreateAPIView` | Create task |
| `/api/projects/tasks/<id>/` | PUT | `TaskDetailAPIView` | Update task |
| `/api/projects/tasks/<id>/` | DELETE | `TaskDetailAPIView` | Delete task |

---

## 5.5 Test It!

> Remember to include the JWT token from login. Replace `<TOKEN>` with your actual access token.

**Create a project:**
```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My First Project", "description": "A test project"}'
```

**List your projects:**
```bash
curl http://127.0.0.1:8000/api/projects/ \
  -H "Authorization: Bearer <TOKEN>"
```

**Create a task:**
```bash
curl -X POST http://127.0.0.1:8000/api/projects/<PROJECT_ID>/tasks/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Fix login bug", "status": "In Progress"}'
```

**Filter tasks by status:**
```bash
curl "http://127.0.0.1:8000/api/projects/<PROJECT_ID>/tasks/?status=Done" \
  -H "Authorization: Bearer <TOKEN>"
```

---

## ✅ What You've Built — The Complete API

You now have a fully functional REST API with:
- ✅ User registration and login with JWT
- ✅ Full CRUD for Projects (ownership-enforced)
- ✅ Full CRUD for Tasks (ownership via parent project)
- ✅ Status filtering for tasks
- ✅ Custom MongoDB JWT authentication backend
- ✅ Two-database architecture (auth_db + project_db)

🎉 **Congratulations — your backend is complete!**

---

## 🔗 Navigation

← **[Previous: Step 4 — Auth Module](./steps_auth_module.md)** · ← **[Back to My Django Project](../my_django_project.md)** · ← **[Back to Main README](../../README.md)**
