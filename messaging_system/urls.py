from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from message.views import MessageListCreateView, MessageRetrieveUpdateDestroyView

urlpatterns = [
    # path("", index),
    path("admin/", admin.site.urls),
    path('api/v1/csrf_cookie/', ensure_csrf_cookie(lambda request: HttpResponse('CSRF cookie set')), name='csrf_cookie'),
    path("api/v1/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/messages/', MessageListCreateView.as_view(filter_backends=[DjangoFilterBackend, OrderingFilter]), name='message-list-create'),
    path('api/v1/messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
