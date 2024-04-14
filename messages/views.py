from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MessageSerializer


@api_view(['POST'])
def write_message(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
