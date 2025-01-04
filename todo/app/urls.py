from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'), # This line maps the home view to the root URL
    path('logout/', views.logoutview, name='logout'), # This line maps the logout view to the /logout URL
    path('register/', views.register, name='register'), # This line maps the register view to the /register URL
    path('login/', views.loginview, name='login'), # This line maps the login view to the /login URL
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'),
    path('update/<str:name>/', views.Update, name='update'),
]
