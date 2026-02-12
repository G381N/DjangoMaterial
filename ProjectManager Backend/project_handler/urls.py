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
