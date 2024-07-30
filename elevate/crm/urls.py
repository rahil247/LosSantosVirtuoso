from django.urls import path
from . import views
from . import utils
from django.urls import path
from django.urls import path
from .views import GoogleLoginView, GoogleCallbackView,login_view
urlpatterns = [
    # path('index',views.index,name='index'),
    path('register.html',views.register,name='register'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('index',views.welcome,name='welcome'),
    path('twt', views.twt, name='twt'),
    path('twm', views.twm, name='twm'),
    path('twf', views.twf, name='twf'),
    path('',views.home,name='home'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('twf', views.twf, name='twf'), 
    #path('send_email', views.send_email,name='send_email'),
    #path('send_email_to_clients', utils.send_email_to_clients,name='send_email_to_clients'),
    path('contact/', views.contact_view, name='contact'),
    path('accounts/google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    path('index', views.welcome, name='welcome'),
    path('login/', login_view, name='login'),
]
