from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title='Authorization API',
      default_version='v1',
      description='Документация использования API сервиса авторизации',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='contact@snippets.local'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('users/', include('users.urls', namespace='users')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
