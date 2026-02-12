from rest_framework.test import APITestCase
from django.urls import reverse
from auth_handler.models import User
from project_handler.models import Project, Task


class ProjectTests(APITestCase):
	def setUp(self):
		# create a test user and get JWT tokens
		url = reverse('auth-register')
		data = {
			'username': 'projectuser',
			'email': 'project@example.com',
			'password': 'securepass',
			'password_confirm': 'securepass'
		}
		resp = self.client.post(url, data, format='json')
		self.assertEqual(resp.status_code, 201)
		self.token = resp.data['access']
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

	def test_create_project(self):
		url = reverse('project-list-create')
		data = {'name': 'My Project', 'description': 'A test project'}
		resp = self.client.post(url, data, format='json')
		self.assertEqual(resp.status_code, 201)
		self.assertIn('project', resp.data)
		self.assertEqual(resp.data['project']['name'], 'My Project')

	def test_list_projects(self):
		# create a project first
		url = reverse('project-list-create')
		self.client.post(url, {'name': 'Project 1'}, format='json')
		# list
		resp = self.client.get(url, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('results', resp.data)
		self.assertEqual(len(resp.data['results']), 1)

	def test_update_project(self):
		# create
		url = reverse('project-list-create')
		resp = self.client.post(url, {'name': 'Old Name'}, format='json')
		project_id = resp.data['project']['id']
		# update
		detail_url = reverse('project-detail', args=[project_id])
		resp2 = self.client.put(detail_url, {'name': 'New Name'}, format='json')
		self.assertEqual(resp2.status_code, 200)
		self.assertEqual(resp2.data['name'], 'New Name')

	def test_delete_project(self):
		# create
		url = reverse('project-list-create')
		resp = self.client.post(url, {'name': 'To Delete'}, format='json')
		project_id = resp.data['project']['id']
		# delete
		detail_url = reverse('project-detail', args=[project_id])
		resp2 = self.client.delete(detail_url, format='json')
		self.assertEqual(resp2.status_code, 204)


class TaskTests(APITestCase):
	def setUp(self):
		# create a test user and get JWT tokens
		url = reverse('auth-register')
		data = {
			'username': 'taskuser',
			'email': 'task@example.com',
			'password': 'securepass',
			'password_confirm': 'securepass'
		}
		resp = self.client.post(url, data, format='json')
		self.assertEqual(resp.status_code, 201)
		self.token = resp.data['access']
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

		# create a project to attach tasks to
		proj_url = reverse('project-list-create')
		proj_resp = self.client.post(proj_url, {'name': 'Task Project'}, format='json')
		self.project_id = proj_resp.data['project']['id']

	def test_create_task(self):
		url = reverse('task-list-create', args=[self.project_id])
		data = {'title': 'My Task', 'description': 'A test task'}
		resp = self.client.post(url, data, format='json')
		self.assertEqual(resp.status_code, 201)
		self.assertIn('task', resp.data)
		self.assertEqual(resp.data['task']['title'], 'My Task')
		self.assertEqual(resp.data['task']['status'], 'Todo')

	def test_list_tasks(self):
		# create a task first
		url = reverse('task-list-create', args=[self.project_id])
		self.client.post(url, {'title': 'Task 1'}, format='json')
		# list
		resp = self.client.get(url, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('results', resp.data)
		self.assertEqual(len(resp.data['results']), 1)

	def test_filter_tasks_by_status(self):
		url = reverse('task-list-create', args=[self.project_id])
		self.client.post(url, {'title': 'Todo Task', 'status': 'Todo'}, format='json')
		self.client.post(url, {'title': 'Done Task', 'status': 'Done'}, format='json')
		# filter
		resp = self.client.get(url + '?status=Done', format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(len(resp.data['results']), 1)
		self.assertEqual(resp.data['results'][0]['title'], 'Done Task')

	def test_update_task(self):
		# create
		url = reverse('task-list-create', args=[self.project_id])
		resp = self.client.post(url, {'title': 'Old Title'}, format='json')
		task_id = resp.data['task']['id']
		# update
		detail_url = reverse('task-detail', args=[task_id])
		resp2 = self.client.put(detail_url, {'title': 'New Title', 'status': 'Done'}, format='json')
		self.assertEqual(resp2.status_code, 200)
		self.assertEqual(resp2.data['title'], 'New Title')
		self.assertEqual(resp2.data['status'], 'Done')

	def test_delete_task(self):
		# create
		url = reverse('task-list-create', args=[self.project_id])
		resp = self.client.post(url, {'title': 'To Delete'}, format='json')
		task_id = resp.data['task']['id']
		# delete
		detail_url = reverse('task-detail', args=[task_id])
		resp2 = self.client.delete(detail_url, format='json')
		self.assertEqual(resp2.status_code, 204)
