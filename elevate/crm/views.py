from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from . forms import Loginform, CustomUserCreationForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from .utils import send_email_to_clients
from google import generativeai as genai
import textwrap
from .models import ChatSession, Message
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from django.views.generic import RedirectView
# import cv2
# import face_recognition
# import numpy as npi


# def face_recognition_view(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         img = face_recognition.load_image_file(file)
#         img_admin = "../../media/img/aryan.jpg"
#         face_encodings = face_recognition.face_encodings(img)
#         if face_encodings:
#             admin_image = face_recognition.load_image_file(img_admin)
#             admin_face_encoding = face_recognition.face_encodings(admin_image)[0]
#             matches = face_recognition.compare_faces([admin_face_encoding], face_encodings[0])
#             if matches[0]:
#                 return JsonResponse({'admin_detected': True})
#             else:
#                 return JsonResponse({'admin_detected': False})
#         return JsonResponse({'admin_detected': False})
#     return JsonResponse({'error': 'Invalid request'}, status=400)
import os
def face_recognition_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        img = face_recognition.load_image_file(file)
        face_encodings = face_recognition.face_encodings(img)
        if face_encodings:
            admin_image_path = os.path.join(settings.MEDIA_ROOT, 'img/aryan.jpg')
            if os.path.exists(admin_image_path):
                admin_image = face_recognition.load_image_file(admin_image_path)
                admin_face_encoding = face_recognition.face_encodings(admin_image)[0]
                matches = face_recognition.compare_faces([admin_face_encoding], face_encodings[0])
                if matches[0]:
                    return JsonResponse({'admin_detected': True})
                else:
                    return JsonResponse({'admin_detected': False})
            else:
                return JsonResponse({'error': 'Admin image not found'}, status=404)
        return JsonResponse({'admin_detected': False})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def send_email(request):
    send_email_to_clients()
    return redirect('/')

# from razorpay import client
from elevate.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY 


from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'crm/register.html', {'registerform': form})

def home(request):
    form = Loginform()
    if request.method =="POST":
        form = Loginform(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('welcome')
    context = {'loginform':form}
    return render(request, 'crm/home.html',context=context)
def user_logout(request):
    logout(request)
    return redirect('home')


client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY ))
def dashboard(request):

    order_amount = 50000
    order_currency = 'INR'
    payment_order = client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture=1))
    payment_order_id = payment_order['id']
    context = {
        'amount':500, 'api_key':RAZORPAY_API_KEY, 'order_id':payment_order_id
    }

    return render(request,'crm/dash.html',context)

def welcome(request):
    if request.method == 'POST':
        selected_personality = request.POST.get('personality','michel')
    return render(request,'crm/welcome.html')


from .forms import ContactForm
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for your message.')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'crm/contact.html',context=context)


# from django.conf import settings
# from django.conf import settings
# from django.shortcuts import redirect
# from django.urls import reverse
# from django.views import View

# class GoogleLoginView(View):
    # def get(self, request, *args, **kwargs):
        # client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
        # redirect_uri = request.build_absolute_uri(reverse('google_callback'))
        # scope = " ".join(settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE'])
        # auth_params = "&".join(f"{k}={v}" for k, v in settings.SOCIALACCOUNT_PROVIDERS['google']['AUTH_PARAMS'].items())
# 
        # google_auth_url = (f"https://accounts.google.com/o/oauth2/auth?"
                        #    f"client_id={client_id}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&{auth_params}")
# 
        # return redirect(google_auth_url)


import requests
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.conf import settings
from django.contrib.auth.models import User
class GoogleLoginView(View):
    def get(self, request, *args, **kwargs):
        client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
        redirect_uri = request.build_absolute_uri(reverse('google_callback'))
        scope = " ".join(settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE'])
        auth_params = "&".join(f"{k}={v}" for k, v in settings.SOCIALACCOUNT_PROVIDERS['google']['AUTH_PARAMS'].items())

        google_auth_url = (f"https://accounts.google.com/o/oauth2/auth?"
                           f"client_id={client_id}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&{auth_params}")

        return redirect(google_auth_url)

class GoogleCallbackView(View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
        client_secret = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret']
        redirect_uri = request.build_absolute_uri(reverse('google_callback'))

        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        user_info_params = {'access_token': access_token}
        user_info_response = requests.get(user_info_url, params=user_info_params)
        user_info = user_info_response.json()

        user_name = user_info['name']
        user_email = user_info['email']
        # first_name = user_info['first_name']

        # Save user info to database and log in the user
        user = self.save_user_to_db(user_name, user_email)

        # Log in the user
        login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

        # Redirect to /index after successful login
        return redirect('/index')
    
    def save_user_to_db(self, user_name, user_email):
        user, created = User.objects.get_or_create(username=user_name,  defaults={'first_name': user_name, 'email': user_email})
        # user, created = User.objects.get_or_create(usern=user_id,  defaults={'first_name': user_name, 'email': user_email})
        if not created:
            user.first_name = user_name
            user.email = user_email
            user.save()
        return user

    # def save_user_to_db(self, user_name, user_email):
    #     # Use email prefix as username and append a unique identifier if necessary
    #     email_prefix = user_email.split('@')[0]
    #     username = email_prefix
    #     counter = 1
    #     while User.objects.filter(username=username).exists():
    #         username = f"{email_prefix}_{counter}"
    #         counter += 1

    #     user, created = User.objects.get_or_create(username=username, defaults={'first_name': user_name, 'email': user_email})
    #     if not created:
    #         user.first_name = user_name
    #         user.email = user_email
    #         user.save()
    #     return user

# class GoogleLoginView(View):
#     def get(self, request, *args, **kwargs):
#         client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
#         redirect_uri = request.build_absolute_uri(reverse('google_callback'))
#         scope = " ".join(settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE'])
#         auth_params = "&".join(f"{k}={v}" for k, v in settings.SOCIALACCOUNT_PROVIDERS['google']['AUTH_PARAMS'].items())

#         google_auth_url = (f"https://accounts.google.com/o/oauth2/auth?"
#                            f"client_id={client_id}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&{auth_params}")

#         return redirect(google_auth_url)

# class GoogleCallbackView(View):
#     def get(self, request, *args, **kwargs):
#         code = request.GET.get('code')
#         client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
#         client_secret = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret']
#         redirect_uri = request.build_absolute_uri(reverse('google_callback'))

#         token_url = 'https://oauth2.googleapis.com/token'
#         token_data = {
#             'code': code,
#             'client_id': client_id,
#             'client_secret': client_secret,
#             'redirect_uri': redirect_uri,
#             'grant_type': 'authorization_code'
#         }
#         token_response = requests.post(token_url, data=token_data)
#         token_json = token_response.json()
#         access_token = token_json.get('access_token')

#         user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
#         user_info_params = {'access_token': access_token}
#         user_info_response = requests.get(user_info_url, params=user_info_params)
#         user_info = user_info_response.json()

#         user_id = user_info['id']
#         user_name = user_info['name']
#         user_email = user_info['email']

#         # Save user info to database and log in the user
#         user = self.save_user_to_db(user_id, user_name, user_email)

#         # Log in the user
#         login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

#         # Redirect to /index after successful login
#         return redirect('/index')

    # def save_user_to_db(self, user_id, user_name, user_email):
    #     user, created = User.objects.get_or_create(username=user_id, defaults={'first_name': user_name, 'email': user_email})
    #     if not created:
    #         user.first_name = user_name
    #         user.email = user_email
    #         user.save()
    #     return user
    
    # def save_user_to_db(self, user_name, user_email):
    #     # Use email prefix as username and append a unique identifier if necessary
    #     email_prefix = user_email.split('@')[0]
    #     username = email_prefix
    #     counter = 1
    #     while User.objects.filter(username=username).exists():
    #         username = f"{email_prefix}_{counter}"
    #         counter += 1

    #     user, created = User.objects.get_or_create(username=username, defaults={'first_name': user_name, 'email': user_email})
    #     if not created:
    #         user.first_name = user_name
    #         user.email = user_email
    #         user.save()
    #     return user

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.http import HttpResponse

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/index')  # Redirect authenticated users to the index page

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Log the user in
            auth_login(request, form.get_user())
            return redirect('/index')
    else:
        form = AuthenticationForm()

    response = render(request, 'crm/home.html', {'loginform': form})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1.
    response['Pragma'] = 'no-cache'  # HTTP 1.0.
    response['Expires'] = '0'  # Proxies.
    return response



# class GoogleLoginView(RedirectView):
#     def get_redirect_url(self, *args, **kwargs):
#         return self.request.build_absolute_uri('/accounts/google/login/')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatSession, Message
from google import generativeai as genai 
from django.urls import reverse
from django.http import HttpResponseRedirect

# Ensure the genai API is configured
genai.configure(api_key='AIzaSyBtvRKafcHnGfXlAndmP2azX_PPqPY9JKo')


class ChatbotSession:
    def __init__(self, personality):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.personality = personality

    def ask_question(self, question):
        # Customize the prompt based on the personality
        personality_prompt = {
            'michel': "You are Michel from GTA V, a balanced and rational character. Only respond to questions related to GTA V.You are a character from GTA 5, not an AI model. Reply to game-related questions only.",
            'trevor': "You are Trevor from GTA V, known for bank robbery and a criminal. Only respond to questions related to GTA V.You are a character from GTA 5, not an AI model. Reply to game-related questions only.",
            'franklin': "You are Franklin from GTA V, a clever and street-smart individual. Only respond to questions related to GTA V. You are a character from GTA 5, not an AI model. Reply to game-related questions only."
        }

        full_question = f"{personality_prompt[self.personality]} {question}"
        response = self.chat.send_message(full_question)

        # Attempt to extract the message from the response
        if hasattr(response, 'message'):
            return response.message
        elif hasattr(response, 'text'):
            return response.text
        else:
            return "No response text found"

@login_required
@csrf_protect
def chat_view(request, personality):
    if request.method == 'POST':
        if 'start_new_session' in request.POST:
            # Create a new session
            ChatSession.objects.create(user=request.user, personality=personality)
            return redirect(f'/tw{personality[0]}')

        message_text = request.POST.get('input_text', '')
        if message_text:
            # Retrieve or create the most recent chat session
            chat_session = ChatSession.objects.filter(user=request.user, personality=personality).order_by('-created_at').first()
            if not chat_session:
                chat_session = ChatSession.objects.create(user=request.user, personality=personality)
            Message.objects.create(chat_session=chat_session, role=request.user.username, text=message_text)
            
            # Initialize ChatbotSession with the selected personality
            chatbot_session = ChatbotSession(personality)
            response_text = chatbot_session.ask_question(message_text)  # Get the response text directly

            if response_text:
                # Save the response in the database
                Message.objects.create(chat_session=chat_session, role=personality.capitalize(), text=response_text)

        return redirect(f'/tw{personality[0]}')
    else:
        chat_session = ChatSession.objects.filter(user=request.user, personality=personality).order_by('-created_at').first()
        chat_history = chat_session.messages.all() if chat_session else []
        context = {
            'chat_history': chat_history,
            'current_personality': personality.capitalize(),
            'username': request.user.username


        }
        return render(request, f'crm/tw{personality[0]}.html', context)

@login_required
def twm(request):
    return chat_view(request, 'michel')

@login_required
def twt(request):
    return chat_view(request, 'trevor')

@login_required
def twf(request):
    return chat_view(request, 'franklin')

@login_required
def chat_history(request):
    chat_sessions = ChatSession.objects.filter(user=request.user).prefetch_related('messages')
    user_display_name = request.user.first_name if request.user.first_name else request.user.username
    return render(request, 'crm/history.html', {'chat_sessions': chat_sessions, 'user_display_name':user_display_name})

@login_required
def delete_chat_history(request, session_id):
    chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    if request.method == 'POST':
        chat_session.delete()
    return HttpResponseRedirect(reverse('chat_history'))