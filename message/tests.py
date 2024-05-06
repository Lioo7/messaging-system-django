from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Message


class MessageModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.user_a = User.objects.create_user(username="alice", password="alicepass")
        self.user_b = User.objects.create_user(username="bob", password="bobpass")

        # Create test message
        self.message = Message.objects.create(
            sender=self.user_a,
            receiver=self.user_b,
            subject="Test Subject",
            content="Test Content",
        )

    def test_message_creation(self):
        self.assertEqual(self.message.sender, self.user_a)
        self.assertEqual(self.message.receiver, self.user_b)
        self.assertEqual(self.message.subject, "Test Subject")
        self.assertEqual(self.message.content, "Test Content")
        self.assertFalse(self.message.is_read)


class MessageAPITests(TestCase):
    def setUp(self):
        # Create test users
        self.user_a = User.objects.create_user(username="alice", password="senderpass")
        self.user_b = User.objects.create_user(username="bob", password="receiverpass")
        self.user_c = User.objects.create_user(
            username="badactor1", password="badactor1pass"
        )
        self.user_d = User.objects.create_user(
            username="badactor2", password="badactor2pass"
        )

        # Create test messages
        message1 = Message.objects.create(
            sender=self.user_a,
            receiver=self.user_b,
            subject="Test Subject 1",
            content="Test Content 1",
            is_read=True,
        )
        message2 = Message.objects.create(
            sender=self.user_b,
            receiver=self.user_a,
            subject="Test Subject 2",
            content="Test Content 2",
            is_read=True,
        )
        message3 = Message.objects.create(
            sender=self.user_b,
            receiver=self.user_a,
            subject="Test Subject 3",
            content="Test Content 3",
        )
        message4 = Message.objects.create(
            sender=self.user_c,
            receiver=self.user_d,
            subject="Test Subject 4",
            content="Test Content 4",
        )
        self.messages = [message1, message2, message3, message4]

        self.client = APIClient()

        # Authenticate the sender user
        self.client.force_authenticate(user=self.user_a)

    def test_create_message_api_success(self):
        # Test successful creation of a message
        data = {
            "sender": self.user_a.id,
            "receiver": self.user_b.id,
            "subject": "Test Subject",
            "content": "Test Content",
        }
        url = reverse("message:message-list-create")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the message was created in the database
        message = Message.objects.last()
        self.assertIsNotNone(message)
        self.assertEqual(message.sender, self.user_a)
        self.assertEqual(message.receiver, self.user_b)
        self.assertEqual(message.subject, "Test Subject")
        self.assertEqual(message.content, "Test Content")

    def test_create_message_api_invalid_data(self):
        # Test creation of a message with invalid data
        data = {
            "sender": self.user_a.id,
            "receiver": self.user_b.id,
        }  # Missing 'subject' and 'content' fields
        url = reverse("message:message-list-create")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_messages_api(self):
        # Test retrieving all messages
        url = reverse("message:message-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_messages_api(self):
        # Test retrieving unread messages (which the receiver is the authenticated user)
        url = reverse("message:message-list-create") + "?is_read=false/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Ensure only one unread message is returned

    def test_read_message_api_success(self):
        # Test reading a message
        message_id = self.messages[1].id  # The second message
        url = reverse("message:message-detail", kwargs={"pk": message_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            response.data["is_read"]
        )  # Ensure the message is marked as read

    def test_read_message_api_message_not_found(self):
        # Test reading a message that doesn't exist
        url = reverse("message:message-detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_message_api_put(self):
        # Test updating a message using PUT method
        message_id = self.messages[0].id  # The first message
        data = {
            "sender": self.user_a.id,
            "receiver": self.user_b.id,
            "subject": "Updated Subject",
            "content": "Updated Content",
        }
        url = reverse("message:message-detail", kwargs={"pk": message_id})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the message was updated in the database
        updated_message = Message.objects.get(id=message_id)
        self.assertEqual(updated_message.subject, "Updated Subject")
        self.assertEqual(updated_message.content, "Updated Content")

    def test_update_another_user_message_forbidden_put(self):
        # Test attempting to update another user's message using PUT method
        message_id = self.messages[1].id  # The second message
        data = {
            "sender": self.user_b.id,
            "receiver": self.user_a.id,
            "subject": "Updated Subject",
            "content": "Updated Content",
        }
        url = reverse("message:message-detail", kwargs={"pk": message_id})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_message_api_patch(self):
        # Test updating a message using PATCH method
        message_id = self.messages[0].id  # The first message
        data = {"subject": "Updated Subject", "content": "Updated Content"}
        url = reverse("message:message-detail", kwargs={"pk": message_id})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the message was updated in the database
        updated_message = Message.objects.get(id=message_id)
        self.assertEqual(updated_message.subject, "Updated Subject")
        self.assertEqual(updated_message.content, "Updated Content")

    def test_update_another_user_message_forbidden_patch(self):
        # Test attempting to update another user's message using PATCH method
        message_id = self.messages[1].id  # The second message
        data = {"subject": "Updated Subject", "content": "Updated Content"}
        url = reverse("message:message-detail", kwargs={"pk": message_id})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_message_api_success(self):
        # Test deleting a message
        message_id = self.messages[1].id  # The second message
        url = reverse("message:message-detail", kwargs={"pk": message_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the message is deleted
        with self.assertRaises(Message.DoesNotExist):
            Message.objects.get(id=message_id)

    def test_delete_message_api_message_not_found(self):
        # Test deleting a message that doesn't exist
        url = reverse("message:message-detail", kwargs={"pk": 99999})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_message_by_unrelated_user_api_forbidden(self):
        # Test attempting to delete a message by a user who is neither the sender nor the receiver
        message_id = self.messages[3].id  # The fourth message
        url = reverse("message:message-detail", kwargs={"pk": message_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        # Test accessing API endpoints without authentication
        self.client.force_authenticate(user=None)  # Remove authentication
        # Attempt to access the messages list endpoint
        url = reverse("message:message-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Attempt to access a specific message endpoint
        message_id = self.messages[0].id
        url = reverse("message:message-detail", kwargs={"pk": message_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
