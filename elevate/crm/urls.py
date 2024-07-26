from django.urls import path
from . import views
from . import utils
urlpatterns = [
    # path('index',views.index,name='index'),
    path('register.html',views.register,name='register'),
    path('',views.my_log,name='my_log'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('welcome',views.welcome,name='welcome'),
    path('twt', views.twt, name='twt'),
    path('twm', views.twm, name='twm'),
    path('twf', views.twf, name='twf'),
    #path('send_email', views.send_email,name='send_email'),
    #path('send_email_to_clients', utils.send_email_to_clients,name='send_email_to_clients'),
    # path('contact/', views.contact_view, name='contact'),
]
