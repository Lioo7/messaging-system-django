import logging
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer

logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.

    POST /api/v1/users/register/
    - Register a new user.
    - Requires providing user data in the request body.
    """
    permission_classes = []  # Allow unauthenticated access
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new user based on the provided data.

        Returns:
        - Response: A response indicating the success or failure of the registration operation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info(f"User {user.id} registered successfully.")

        return Response({
            'message': 'User registration successful.',
            'user_id': user.id
        })
