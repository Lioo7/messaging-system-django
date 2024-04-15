from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from messaging.views import write_message, get_all_messages, get_unread_messages, read_message, delete_message

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/messaging/write/", write_message),
    path("api/messaging/messages/", get_all_messages),
    path("api/messaging/messages/unread/", get_unread_messages),
    path("api/messaging/messages/<int:message_id>/read/", read_message),
    path("api/messaging/messages/<int:message_id>/delete/", delete_message)
]
