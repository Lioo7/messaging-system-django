from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Messaging
from .serializers import MessagingSerializer


class MessagingModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.user_a = User.objects.create_user(username='alice', password='alicepass')
        self.user_b = User.objects.create_user(username='bob', password='bobpass')

        # Create test message
        self.message = Messaging.objects.create(
            sender=self.user_a,
            receiver=self.user_b,
            subject='Test Subject',
            content='Test Content'
        )

    def test_message_creation(self):
        self.assertEqual(self.message.sender, self.user_a)
        self.assertEqual(self.message.receiver, self.user_b)
        self.assertEqual(self.message.subject, 'Test Subject')
        self.assertEqual(self.message.content, 'Test Content')
        self.assertFalse(self.message.is_read)


class MessagingAPITests(TestCase):
    def setUp(self):
        # Create test users
        self.user_a = User.objects.create_user(username='alice', password='senderpass')
        self.user_b = User.objects.create_user(username='bob', password='receiverpass')

        # Create test messages
        message1 = Messaging.objects.create(sender=self.user_a, receiver=self.user_b, subject='Test Subject 1', content='Test Content 1', is_read=True)
        message2 = Messaging.objects.create(sender=self.user_b, receiver=self.user_a, subject='Test Subject 2', content='Test Content 2')
        self.messages = [message1, message2]

        self.client = APIClient()

        # Authenticate the sender user
        self.client.force_authenticate(user=self.user_a)

    def test_write_message_api_success(self):
        # Test successful creation of a message
        data = {'sender': self.user_a.id, 'receiver': self.user_b.id, 'subject': 'Test Subject', 'content': 'Test Content'}
        response = self.client.post('/api/messaging/write/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the message was created in the database
        message = Messaging.objects.last()
        self.assertIsNotNone(message)
        self.assertEqual(message.sender, self.user_a)
        self.assertEqual(message.receiver, self.user_b)
        self.assertEqual(message.subject, 'Test Subject')
        self.assertEqual(message.content, 'Test Content')

    def test_write_message_api_invalid_data(self):
        # Test creation of a message with invalid data
        data = {'sender': self.user_a.id, 'receiver': self.user_b.id}  # Missing 'subject' and 'content' fields
        response = self.client.post('/api/messaging/write/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_write_message_api_unauthenticated(self):
        # Test creating a message without authentication
        self.client.force_authenticate(user=None)  # Remove authentication
        data = {'sender': self.user_a.id, 'receiver': self.user_b.id, 'subject': 'Test Subject', 'content': 'Test Content'}
        response = self.client.post('/api/messaging/write/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_messages_api(self):
        # Test retrieving all messages
        response = self.client.get('/api/messaging/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.messages))

    def test_get_unread_messages_api(self):
        # Test retrieving unread messages (which the receiver is the authenticated user)
        response = self.client.get('/api/messaging/messages/unread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure only one unread message is returned

    def test_read_message_api_success(self):
        # Test reading a message
        message_id = self.messages[1].id # The second message
        response = self.client.get(f'/api/messaging/messages/{message_id}/read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_read'])  # Ensure the message is marked as read

    def test_read_message_api_message_not_found(self):
        # Test reading a message that doesn't exist
        response = self.client.get('/api/messaging/messages/99999/read/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_message_api_success(self):
        # Test deleting a message
        message_id = self.messages[1].id # The second message
        response = self.client.delete(f'/api/messaging/messages/{message_id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the message is deleted
        with self.assertRaises(Messaging.DoesNotExist):
            Messaging.objects.get(id=message_id)

    def test_delete_message_api_message_not_found(self):
        # Test deleting a message that doesn't exist
        response = self.client.delete('/api/messaging/messages/99999/delete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
