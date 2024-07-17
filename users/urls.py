from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('create/', views.UserAuthorization.as_view(), name='user_create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('verification_phone/', views.UserVerificationPhone.as_view(), name='verification_phone'),
]
