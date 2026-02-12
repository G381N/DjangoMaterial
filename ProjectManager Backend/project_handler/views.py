

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from project_handler.models import Project, Task
from project_handler.serializers import ProjectSerializer, TaskSerializer


# checks if all required keys are present in the request data, returns 400 response if any are missing
def validate_keys(data, required_keys):
	missing_keys = [key for key in required_keys if key not in data]
	if missing_keys:
		return Response(
			{
				"message": "There is a Missing Field ...",
				"missing_fields": missing_keys,
			},
			status=status.HTTP_400_BAD_REQUEST,
		)
	return None

#List all projects for the logged-in user or create a new project.

class ProjectListCreateAPIView(APIView):
	permission_classes = (IsAuthenticated,)

	# returns a list of all projects owned by the currently logged-in user
	def get(self, request):
		# Variables---------------------------------------------------------------------------------------------------
		user = request.user
		# Fetching projects owned by user-----------------------------------------------------------------------------
		projects_under_user = Project.objects.filter(owner=user)
		data = ProjectSerializer(projects_under_user, many=True).data
		return Response({"results": data}, status=status.HTTP_200_OK)

	# creates a new project with the current user automatically set as the owner
	def post(self, request):
		# Variables---------------------------------------------------------------------------------------------------
		data = request.data or {}
		name = data.get("name")
		description = data.get("description")

		# Checking if any field is empty------------------------------------------------------------------------------		
		req = ("name",)  #RequiredList
		missing = validate_keys(data, req)
		# if there is any field missing missing_response wont be empty and will print the response
		if missing:
			return missing

		# all validations passed now we create project object and save once-------------------------------------------
		user = request.user #getting form backend.py i.e the jwt handler
		project = Project()
		try:
			project.name = name
			if description:
				project.description = description
			project.owner = user
			project.save()
		except Exception:
			return Response({"detail": "Failed to create project ..."}, status=status.HTTP_400_BAD_REQUEST)

		return Response(
			{
				"project": ProjectSerializer(project).data,
				"message": "Project Created Successfully ..."
			},
			status=status.HTTP_201_CREATED,
		)


#Update or delete a specific project (owner only).

class ProjectDetailAPIView(APIView):
	permission_classes = (IsAuthenticated,)

	# helper to fetch a single project by its id, returns None if not found
	def get_object(self, project_id):
		return Project.objects.filter(id=project_id).first()

	# retrieve a single project
	def get(self, request, project_id):
		project = self.get_object(project_id)
		if not project:
			return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
		if project.owner != request.user:
			return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
		return Response(ProjectSerializer(project).data, status=status.HTTP_200_OK)

	# updates an existing project's name/description, only if the requesting user is the owner
	def put(self, request, project_id):
		# Variables---------------------------------------------------------------------------------------------------
		project = self.get_object(project_id)
		# Checking if project exists----------------------------------------------------------------------------------
		if not project:
			return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
		# Checking ownership------------------------------------------------------------------------------------------
		if project.owner != request.user:
			return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
		# Other validations-------------------------------------------------------------------------------------------
		raw = request.data or {}
		name = raw.get("name")
		description = raw.get("description")
		if name:
			project.name = name
		if description is not None:
			project.description = description
		project.save()
		return Response(ProjectSerializer(project).data, status=status.HTTP_200_OK)

	# deletes a project permanently, only if the requesting user is the owner
	def delete(self, request, project_id):
		# Variables---------------------------------------------------------------------------------------------------
		project = self.get_object(project_id)
		# Checking if project exists----------------------------------------------------------------------------------
		if not project:
			return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
		# Checking ownership------------------------------------------------------------------------------------------
		if project.owner != request.user:
			return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
		project.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


#List all tasks for a project or create a new task under a project.

class TaskListCreateAPIView(APIView):
	permission_classes = (IsAuthenticated,)

	# lists all tasks under a project, supports optional ?status= query param for filtering
	def get(self, request, project_id):
		# Variables---------------------------------------------------------------------------------------------------
		project = Project.objects.filter(id=project_id).first()
		# Checking if project exists----------------------------------------------------------------------------------
		if not project:
			return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
		# Checking ownership------------------------------------------------------------------------------------------
		if project.owner != request.user:
			return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
		# Filtering by status (optional)------------------------------------------------------------------------------
		status_filter = request.query_params.get("status") # in param we can pass status=Done, Todo, In Progress
		tasks_in_project = Task.objects.filter(project=project)
		if status_filter:
			tasks_in_project = tasks_in_project.filter(status=status_filter)
		data = TaskSerializer(tasks_in_project, many=True).data
		return Response({"results": data}, status=status.HTTP_200_OK)

	# creates a new task under the given project, only if the requesting user owns the project
	def post(self, request, project_id):
		# Variables---------------------------------------------------------------------------------------------------
		project = Project.objects.filter(id=project_id).first()
		# Checking if project exists----------------------------------------------------------------------------------
		if not project:
			return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
		# Checking ownership------------------------------------------------------------------------------------------
		if project.owner != request.user:
			return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
		# Checking if any field is empty------------------------------------------------------------------------------
		raw = request.data or {}
		req = ("title",)  #RequiredList
		missing = validate_keys(raw, req)
		# if there is any field missing missing_response wont be empty and will print the response
		if missing:
			return missing

		title = raw.get("title")
		description = raw.get("description")
		status_val = raw.get("status") or "Todo"

		# all validations passed now we create task object and save once----------------------------------------------
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

		return Response(
			{
				"task": TaskSerializer(task).data,
				"message": "Task Created Successfully ..."
			},
			status=status.HTTP_201_CREATED,
		)


#Update or delete a specific task (project owner only).

class TaskDetailAPIView(APIView):
	permission_classes = (IsAuthenticated,)

	# helper to fetch a single task by its id, returns None if not found
	def get_object(self, task_id):
		return Task.objects.filter(id=task_id).first()

	# updates an existing task's title/description/status, only if the user owns the parent project
	def put(self, request, task_id):
		# Variables---------------------------------------------------------------------------------------------------
		task = self.get_object(task_id)
		# Checking if task exists-------------------------------------------------------------------------------------
		if not task:
			return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
		# Checking ownership (via project.owner)----------------------------------------------------------------------
		if task.project.owner != request.user:
			return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
		# Other validations-------------------------------------------------------------------------------------------
		raw = request.data or {}
		title = raw.get("title")
		description = raw.get("description")
		status_val = raw.get("status")
		if title:
			task.title = title
		if description is not None:
			task.description = description
		if status_val:
			task.status = status_val
		task.save()
		return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

	# deletes a task permanently, only if the user owns the parent project
	def delete(self, request, task_id):
		# Variables---------------------------------------------------------------------------------------------------
		task = self.get_object(task_id)
		# Checking if task exists-------------------------------------------------------------------------------------
		if not task:
			return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
		# Checking ownership (via project.owner)----------------------------------------------------------------------
		if task.project.owner != request.user:
			return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
		task.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
