from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from message.views import get_csrf_token

urlpatterns = [
    path('', include('message.urls')),
    path('api/v1/accounts/', include('accounts.urls')),
    path("admin/", admin.site.urls),
    # path('api/v1/csrf_cookie/', get_csrf_token, name='csrf_cookie'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
