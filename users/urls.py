from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('create/', views.UserInputPhoneView.as_view(), name='user_create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('verification_phone/', views.UserVerificationPhoneView.as_view(), name='verification_phone'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
]
