from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('password/', views.password, name="password"),
    path('change/', views.change, name="change"),
    path('like/<int:actor_pk>/', views.like, name="like"),
    path('profile/<int:user_id>/', views.profile, name="profile"),
]