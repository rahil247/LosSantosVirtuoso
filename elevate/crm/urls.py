from django.urls import path
from . import views
urlpatterns = [
    path('index',views.home,name='home'),
    path('register',views.register,name='register'),
    path('',views.my_log,name='my_log'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('user_logout',views.user_logout,name='user_logout'),
]
