import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .utils import get_messages
from .serializers import MessageSerializer
from .filters import MessageFilter

logger = logging.getLogger(__name__)


class RootView(APIView):
    """
    API endpoint to provide root information about the Messaging System API.
    """

    permission_classes = []  # Allow unauthenticated access

    def get(self, request):
        """
        Get method to provide information about the API endpoints.

        Returns:
        - Response: A response containing information about the API endpoints.
        """
        logger.info("Received request for API root information.")

        # Assuming there is a message instance with pk=1
        message_pk = 1
        return Response({
            'message': 'Welcome to the Messaging System API!',
            'endpoints': {
                'messages': {
                    'list_create': reverse('message-list-create', request=request),
                    'retrieve_update_destroy': reverse('message-detail', kwargs={'pk': message_pk}, request=request),
                },
                'token': {
                    'obtain': reverse('token_obtain_pair', request=request,),
                    'refresh': reverse('token_refresh', request=request),
                },
                'csrf_cookie': reverse('csrf_cookie', request=request),
            }
        })


class MessageListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating messages.

    GET /api/v1/messages/
    - List messages associated with the authenticated user.
    - Supports filtering by read/unread status using the `is_read` query parameter.

    POST /api/v1/messages/
    - Create a new message.
    - Requires authentication.
    - The `sender` field is automatically set to the authenticated user.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_class = MessageFilter

    def get_queryset(self):
        """
        Get the queryset of messages based on the currently authenticated user and query parameters.

        Returns:
        - QuerySet: A queryset of messages associated with the given user.
        """
        user = self.request.user
        logger.info(f"Retrieving messages for user: {user}")
        is_read = self.request.query_params.get('is_read', None)
        # TODO: modify the get_messages function
        queryset = get_messages(user)

        if is_read is not None:
            # Convert the 'is_read' parameter value to a boolean
            is_read_bool = is_read.lower() == 'true/'
            # Filter the queryset based on whether the message is read or unread
            queryset = queryset.filter(receiver=user, is_read=is_read_bool)

        return queryset

    def perform_create(self, serializer):
        """
        Perform creation of a message and set the sender as the currently authenticated user.
        """
        logger.info(f"Creating new message for user: {self.request.user}")
        serializer.save(sender=self.request.user)
        logger.info(f"New message created: {serializer.data}")


class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting messages.

    GET /api/v1/messages/{id}/
    - Retrieve a specific message.
    - If the authenticated user is the receiver, the message will be marked as read.
    - Requires authentication.

    PUT /api/v1/messages/{id}/
    - Update a specific message.
    - Only the sender of the message can update it.
    - Requires authentication.

    PATCH /api/v1/messages/{id}/
    - Partially update a specific message.
    - Only the sender of the message can update it.
    - Requires authentication.

    DELETE /api/v1/messages/{id}/
    - Delete a specific message.
    - Requires authentication.
    - Only the sender or the receiver of the message can delete it.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """
        Get the queryset of messages based on the currently authenticated user.

        Returns:
        - QuerySet: A queryset of messages associated with the given user.
        """
        user = self.request.user
        logger.info(f"Retrieving messages for user: {user}")
        return get_messages(user)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a message and mark it as read if the receiver is the currently authenticated user.

        Returns:
        - Response: A response containing the retrieved message.
        """
        instance = self.get_object()
        if instance.receiver == request.user:
            instance.is_read = True
            instance.save()
            logger.info(f"Marked message as read: {instance.id}")
        serializer = self.get_serializer(instance)
        logger.info(f"Retrieved message: {serializer.data}")
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update a message if the sender is the currently authenticated user.

        Returns:
        - Response: A response containing the updated message or an error message.
        """
        instance = self.get_object()

        if instance.sender != request.user:
            logger.warning(f"User {request.user} attempted to update message {instance.id} but is not authorized.")
            return Response({"message": "You are not authorized to update this message."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info(f"Message {instance.id} updated by user {request.user}")

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a message.

        Returns:
        - Response: A response indicating the success or failure of the deletion operation.
        """

        instance = self.get_object()
        logger.info(f"Deleting message {instance.id} by user {request.user}")
        self.perform_destroy(instance)

        return Response({"message": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
