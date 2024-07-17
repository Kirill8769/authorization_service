from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('create/', views.UserAuthorization.as_view(), name='user_create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('verify_phone/', views.UserVerifyPhone.as_view(), name='verify_phone'),
]
