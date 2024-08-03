from django.urls import path
from . import views
from . import utils
from django.urls import path
from django.urls import path
from .views import GoogleLoginView, GoogleCallbackView,login_view
urlpatterns = [
    # path('index',views.index,name='index'),
    path('register.html',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('index/',views.welcome,name='welcome'),
    path('twt', views.twt, name='twt'),
    path('twm', views.twm, name='twm'),
    path('twf', views.twf, name='twf'),
    path('',views.home,name='home'),
    path('user_logout',views.user_logout,name='user_logout'),
    # path('twf', views.twf, name='twf'), 
    #path('send_email', views.send_email,name='send_email'),
    #path('send_email_to_clients', utils.send_email_to_clients,name='send_email_to_clients'),
    path('contact/', views.contact_view, name='contact'),
    path('accounts/google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    # path('index/', views.welcome, name='welcome'),
    path('login/', login_view, name='login'),
    path('history/', views.chat_history, name='chat_history'),
    path('delete_chat_history/<int:session_id>/', views.delete_chat_history, name='delete_chat_history'),
]

# changes register.html to register/ , dashboard to dashboard/, index to index/, twt to chat/trevor/, twm to chat/michel/, twf to chat/franklin/, user_logout to user_logout/, added path('history/', views.chat_history, name='chat_history'),