from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_user_registration_success(self):
        """
        Test that a user can be registered successfully.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User registration successful.')
        self.assertIsNotNone(response.data['user_id'])
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)

    def test_user_registration_missing_data(self):
        """
        Test that a user cannot be registered with missing data.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_username(self):
        """
        Test that a user cannot be registered with a duplicate username.
        """
        User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        data = {
            'username': 'testuser',
            'email': 'another@example.com',
            'password': 'anotherpassword'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
