from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="AIRecipeGenerator API",
      default_version='v1',
      description="API ChefMate предоставляет доступ к различным запросам, требующим аутентификации "
                  "с помощью токена Bearer. "
                  "Для аутентификации включите 'Bearer {access_token}' в заголовок 'Authorization'.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^chefmate/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^chefmate/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^chefmate/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('chefmate/admin/', admin.site.urls),
    path('chefmate/users/', include('authentication.urls')),
    path('chefmate/grocery/', include('grocery.urls')),
    path('chefmate/ingredients/', include('ingredients.urls')),
]
