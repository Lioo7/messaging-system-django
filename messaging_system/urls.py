from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from messaging.views import index, write_message, get_all_messages, get_unread_messages, read_message, delete_message


urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/messaging/write/", write_message, name='write_message'),
    path("api/messaging/messages/", get_all_messages, name='get_all_messages'),
    path("api/messaging/messages/unread/", get_unread_messages, name='get_unread_messages'),
    path("api/messaging/messages/<int:message_id>/read/", read_message, name='read_message'),
    path("api/messaging/messages/<int:message_id>/delete/", delete_message, name='delete_message')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
