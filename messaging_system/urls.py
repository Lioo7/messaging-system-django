from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Include your app's URLs
    path("", include("message.urls")),
    path("api/v1/accounts/", include("accounts.urls")),

    # Include Swagger URLs
    path("", include("messaging_system.swagger_urls")),

    # Django admin
    path("admin/", admin.site.urls),

    # JWT token URLs
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Redirect root URL to Swagger page
    path("", RedirectView.as_view(url="/swagger/", permanent=False)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
