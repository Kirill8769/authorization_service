from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('authorization/', views.UserAuthorizationView.as_view(), name='user_authorization'),
    path('verification/', views.UserVerificationPhoneView.as_view(), name='user_verification'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),

    path('api_list/', views.UserListAPIView.as_view(), name='user_api_list'),
    path('api_authorization/', views.UserAuthorizationAPIView.as_view(), name='user_api_authorization'),
    path('api_verification/', views.UserVerificationAPIView.as_view(), name='user_api_verification'),
    path('api_detail/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user_api_detail'),
    path('api_update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user_api_update'),
]
