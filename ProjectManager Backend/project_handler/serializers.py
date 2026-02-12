from rest_framework_mongoengine.serializers import DocumentSerializer
from project_handler.models import Project, Task
from rest_framework.exceptions import ValidationError


# minimal project serializer — owner is read-only, auto-set from request.user in views
class ProjectSerializer(DocumentSerializer):
	class Meta:
		model = Project
		fields = ("id", "name", "description", "owner", "created_at")
		read_only_fields = ("id", "owner", "created_at")


# task serializer — status limited to valid choices
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

# Notes:
# - ProjectSerializer is used for both list and detail responses.
# - TaskSerializer validates the status field against allowed choices.
# - owner and project fields are read-only so they can only be set in the view logic,
#   preventing users from assigning projects/tasks to other users.
