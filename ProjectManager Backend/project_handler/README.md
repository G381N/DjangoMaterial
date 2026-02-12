# Project Handler

The `project_handler` app manages **Projects** and **Tasks** for authenticated users. It enforces ownership-based permissions — users can only access their own projects and the tasks within them.

---

## File Structure

```
project_handler/
├── __init__.py
├── apps.py            # Django app configuration
├── models.py          # MongoEngine documents: Project, Task
├── serializers.py     # DRF-MongoEngine serializers for Project & Task
├── views.py           # APIView-based views for CRUD operations
├── urls.py            # URL routing for project & task endpoints
├── tests.py           # Test cases for all CRUD + filtering
└── README.md          # This file
```

---

## Models (`models.py`)

Both models use `mongoengine.Document` and are stored in the `project_db` MongoDB database.

### Project

| Field         | Type             | Notes                              |
|---------------|------------------|------------------------------------|
| `name`        | `StringField`    | Required                           |
| `description` | `StringField`    | Optional                           |
| `owner`       | `ReferenceField` | Points to `auth_handler.User`      |
| `created_at`  | `DateTimeField`  | Auto-set to `datetime.utcnow`      |

### Task

| Field         | Type             | Notes                                        |
|---------------|------------------|----------------------------------------------|
| `title`       | `StringField`    | Required                                     |
| `description` | `StringField`    | Optional                                     |
| `status`      | `StringField`    | Choices: `Todo`, `In Progress`, `Done`       |
| `project`     | `ReferenceField` | Points to `Project`                          |
| `created_at`  | `DateTimeField`  | Auto-set to `datetime.utcnow`                |

---

## Serializers (`serializers.py`)

Uses `DocumentSerializer` from `rest_framework_mongoengine` (same pattern as `auth_handler`).

- **`ProjectSerializer`** — Exposes `id`, `name`, `description`, `owner`, `created_at`. The `owner` and `created_at` fields are **read-only** (owner is auto-set from `request.user` in the view).
- **`TaskSerializer`** — Exposes `id`, `title`, `description`, `status`, `project`, `created_at`. The `project` and `created_at` fields are **read-only**. Includes a `validate_status()` method to ensure only valid choices are accepted.

---

## Views (`views.py`)

All views are **class-based** using DRF's `APIView` and require `IsAuthenticated` permission.

### Key Pattern: `objects.filter()` for Queries

All database lookups use `Model.objects.filter(...)` instead of `Model.objects(...)` for explicit clarity about query operations.

### Helper Function

- **`validate_keys(data, required_keys)`** — Checks for missing required fields in request data. Returns a `400 Bad Request` response listing the missing fields, or `None` if all keys are present.

### Project Views

#### `ProjectListCreateAPIView`

| Method | Endpoint             | Description                                         |
|--------|----------------------|-----------------------------------------------------|
| `GET`  | `/api/projects/`     | List all projects for the logged-in user             |
| `POST` | `/api/projects/`     | Create a new project (owner auto-set to current user)|

**GET flow:**
1. Get `request.user`
2. `Project.objects.filter(owner=user)` — fetch only this user's projects
3. Serialize and return

**POST flow:**
1. Validate required fields (`name`)
2. Create `Project` object, set `name`, `description`, `owner`
3. Save and return serialized project + success message

#### `ProjectDetailAPIView`

| Method   | Endpoint                  | Description                        |
|----------|---------------------------|------------------------------------|
| `PUT`    | `/api/projects/:project_id/`      | Update project (owner only)        |
| `DELETE` | `/api/projects/:project_id/`      | Delete project (owner only)        |

**Flow for both:**
1. `Project.objects.filter(id=project_id).first()` — find the project
2. Check existence → `404` if not found
3. Check `project.owner != request.user` → `403` if forbidden
4. Update fields / delete

### Task Views

#### `TaskListCreateAPIView`

| Method | Endpoint                          | Description                                   |
|--------|-----------------------------------|-----------------------------------------------|
| `GET`  | `/api/projects/:project_id/tasks/`        | List tasks for project (supports `?status=`)  |
| `POST` | `/api/projects/:project_id/tasks/`        | Create a task under the project               |

**GET supports filtering:** Pass `?status=Done` (or `Todo`, `In Progress`) as a query parameter to filter tasks by status.

#### `TaskDetailAPIView`

| Method   | Endpoint                          | Description                        |
|----------|-----------------------------------|------------------------------------|
| `PUT`    | `/api/projects/tasks/:task_id/`        | Update task (project owner only)   |
| `DELETE` | `/api/projects/tasks/:task_id/`        | Delete task (project owner only)   |

**Ownership check for tasks:** The view checks `task.project.owner != request.user` — meaning ownership is verified through the parent project, not directly on the task.

---

## URLs (`urls.py`)

All routes are mounted under `/api/projects/` via the core `ProjectManagerCore/urls.py`.

```python
path("", ProjectListCreateAPIView.as_view(), name="project-list-create")
path("<str:project_id>/", ProjectDetailAPIView.as_view(), name="project-detail")
path("<str:project_id>/tasks/", TaskListCreateAPIView.as_view(), name="task-list-create")
path("tasks/<str:task_id>/", TaskDetailAPIView.as_view(), name="task-detail")
```

### Full URL Map

| Full URL                             | View                       | Name                  |
|--------------------------------------|----------------------------|-----------------------|
| `/api/projects/`                     | `ProjectListCreateAPIView` | `project-list-create` |
| `/api/projects/:project_id/`                | `ProjectDetailAPIView`     | `project-detail`      |
| `/api/projects/:project_id/tasks/`          | `TaskListCreateAPIView`    | `task-list-create`    |
| `/api/projects/tasks/:task_id/`          | `TaskDetailAPIView`        | `task-detail`         |

---

## Tests (`tests.py`)

Uses `APITestCase` with JWT authentication (same pattern as `auth_handler` tests).

### ProjectTests
- `test_create_project` — POST a new project, verify `201` and response data
- `test_list_projects` — Create then GET, verify list contains 1 result
- `test_update_project` — Create then PUT with new name, verify update
- `test_delete_project` — Create then DELETE, verify `204`

### TaskTests
- `test_create_task` — POST a task under a project, verify `201` and default `Todo` status
- `test_list_tasks` — Create then GET, verify list
- `test_filter_tasks_by_status` — Create tasks with different statuses, filter by `?status=Done`
- `test_update_task` — Create then PUT with new title and status, verify update
- `test_delete_task` — Create then DELETE, verify `204`

---

## Response Shapes

### Success (Create)
```json
{
  "project": {
    "id": "...",
    "name": "My Project",
    "description": "...",
    "owner": "...",
    "created_at": "..."
  },
  "message": "Project Created Successfully ..."
}
```

### Success (List)
```json
{
  "results": [
    { "id": "...", "name": "...", ... }
  ]
}
```

### Error (Missing Fields)
```json
{
  "message": "There is a Missing Field ...",
  "missing_fields": ["name"]
}
```

### Error (Not Found / Forbidden)
```json
{
  "detail": "Not found"
}
```

---

## Permissions & Security

- **All endpoints require JWT authentication** (`IsAuthenticated`)
- **Ownership enforcement:** Users can only see/modify their own projects
- **Task ownership via project:** Task operations check `task.project.owner == request.user`
- **No cross-user access:** Listing filters by `owner=request.user`

---

## How It Connects

```
request → ProjectManagerCore/urls.py → project_handler/urls.py → views.py → models.py ↔ MongoDB (project_db)
                                                                          → serializers.py (data shaping)
                                                                          ← Response (JSON)
```
