from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Messaging
from .serializers import MessagingSerializer


class MessagingModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.sender_user = User.objects.create_user(username='sender', password='senderpass')
        self.receiver_user = User.objects.create_user(username='receiver', password='receiverpass')

        # Create test message
        self.message = Messaging.objects.create(
            sender=self.sender_user,
            receiver=self.receiver_user,
            subject='Test Subject',
            content='Test Content'
        )

    def test_message_creation(self):
        self.assertEqual(self.message.sender, self.sender_user)
        self.assertEqual(self.message.receiver, self.receiver_user)
        self.assertEqual(self.message.subject, 'Test Subject')
        self.assertEqual(self.message.content, 'Test Content')
        self.assertFalse(self.message.is_read)
