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

