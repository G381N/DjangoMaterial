from rest_framework.test import APITestCase
from django.urls import reverse
from auth_handler.models import User


class AuthTests(APITestCase):
	def test_register_and_login(self):
		url = reverse('auth-register')
		data = {
			'username': 'testuser',
			'email': 'test@example.com',
			'password': 'securepass',
			'password_confirm': 'securepass'
		}
		resp = self.client.post(url, data, format='json')
		self.assertEqual(resp.status_code, 201)
		self.assertIn('access', resp.data)
		self.assertIn('refresh', resp.data)

		# login
		url = reverse('auth-login')
		resp2 = self.client.post(url, {'email': 'test@example.com', 'password': 'securepass'}, format='json')
		self.assertEqual(resp2.status_code, 200)
		self.assertIn('access', resp2.data)
		self.assertIn('refresh', resp2.data)
