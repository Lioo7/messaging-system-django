from django.urls import path
from .views import RootView, MessageListCreateView, MessageRetrieveUpdateDestroyView

app_name = 'message'

urlpatterns = [
    path('', RootView.as_view(), name='api-root'),
    path('api/v1/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('api/v1/messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),
]
