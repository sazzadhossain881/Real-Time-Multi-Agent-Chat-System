from django.urls import path
from user import views

urlpatterns = [
    path("register/", views.RegisterAPIView.as_view(), name='register-view'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("profile/", views.UserProfileAPIView.as_view(), name='user-profile'),
]
