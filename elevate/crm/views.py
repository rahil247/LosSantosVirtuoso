from typing import Any
from django.db.models.query import QuerySet
from .forms import Loginform, CustomUserCreationForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from google import generativeai as genai
import textwrap
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from django.views.generic import RedirectView
from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatSession, Message
from django.urls import reverse
from django.http import HttpResponseRedirect
# from razorpay import client
from elevate.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
import requests
from django.views import View
from django.contrib.auth.models import User
import streamlit as st
from google.generativeai import generative_models, types
from google.generativeai import generative_models, configure
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import ChatSession, Message


# View to handle user registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'crm/register.html', {'registerform': form})

# View for user login
def home(request):
    form = Loginform()
    if request.method == "POST":
        form = Loginform(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('welcome')
    context = {'loginform': form}
    return render(request, 'crm/home.html', context=context)

# View for user logout
def user_logout(request):
    logout(request)
    return redirect('home')

# Razorpay client setup for payment processing
client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

# Dashboard view to handle payment orders
def dashboard(request):
    order_amount = 50000
    order_currency = 'INR'
    payment_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))
    payment_order_id = payment_order['id']
    context = {
        'amount': 500, 'api_key': RAZORPAY_API_KEY, 'order_id': payment_order_id
    }
    return render(request, 'crm/dash.html', context)

# View for welcome page after login
def welcome(request):
    if request.method == 'POST':
        selected_personality = request.POST.get('personality', 'michel')
    return render(request, 'crm/welcome.html')

# View to handle contact form submissions
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
    return render(request, 'crm/contact.html', context=context)

# Google OAuth2 login view
class GoogleLoginView(View):
    def get(self, request, *args, **kwargs):
        client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
        redirect_uri = request.build_absolute_uri(reverse('google_callback'))
        scope = " ".join(settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE'])
        auth_params = "&".join(f"{k}={v}" for k, v in settings.SOCIALACCOUNT_PROVIDERS['google']['AUTH_PARAMS'].items())

        google_auth_url = (f"https://accounts.google.com/o/oauth2/auth?"
                           f"client_id={client_id}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&{auth_params}")

        return redirect(google_auth_url)

# Google OAuth2 callback view
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
        user = self.save_user_to_db(user_name, user_email)

        login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

        return redirect('/index')
    
    def save_user_to_db(self, user_name, user_email):
        user, created = User.objects.get_or_create(username=user_name,  defaults={'first_name': user_name, 'email': user_email})
        if not created:
            user.first_name = user_name
            user.email = user_email
            user.save()
        return user

# View for handling user login using Django authentication
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/index')  

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Log the user in
            auth_login(request, form.get_user())
            return redirect('/index')
    else:
        form = AuthenticationForm()

    response = render(request, 'crm/home.html', {'loginform': form})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  
    response['Pragma'] = 'no-cache'  
    response['Expires'] = '0'  
    return response

genai.configure(api_key="AIzaSyBtvRKafcHnGfXlAndmP2azX_PPqPY9JKo")


# Class to handle chat sessions with different personalities
class ChatbotSession:
    def __init__(self, personality):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.personality = personality

    def ask_question(self, question):
        personality_prompt = {
            'michel': (
                "You are Michael De Santa from GTA V. You are a retired bank robber turned family man, trying to navigate a midlife crisis. "
                "You have a complex relationship with your family and a longing for your criminal past. "
                "You are rational, yet nostalgic, and often reflect on your past heists and the golden days of your criminal career. "
                "Only respond to questions related to GTA V with the mindset and experiences of Michael De Santa. "
                "You are a character from GTA 5, not an AI model. "
                "Please reply safely and do not use inappropriate language."
                "do not use any cuss language. if you find such questions don't respond to it"
                "follow safety and security setting if the gemini do not violate it."
                "do not give any response to questions regarding killing,threating,guns etc"
            ),
            'trevor': (
                "You are Trevor Philips from GTA V. You are a volatile and unpredictable character, known for your violent outbursts and criminal exploits. "
                "You have a deep-seated loyalty to your friends, especially Michael, despite feeling betrayed by him in the past. "
                "Your life is chaotic, filled with dangerous adventures and a constant pursuit of power and thrills. "
                "Only respond to questions related to GTA V with the intensity and erratic nature of Trevor Philips. "
                "You are a character from GTA 5, not an AI model. "
                "Please reply safely and do not use inappropriate language."
                "do not use any cuss language. if you find such questions don't respond to it"
                "follow safety and security setting if the gemini do not violate it."
                "do not give any response to questions regarding killing,threating,guns etc"
            ),
            'franklin': (
                "You are Franklin Clinton from GTA V. You are a young, ambitious hustler from the streets of Los Santos, seeking a better life. "
                "You are smart, resourceful, and always looking for opportunities to rise above your circumstances. "
                "Your experiences in the gang life have made you tough, but you also have a strong sense of loyalty and a desire for something greater. "
                "Only respond to questions related to GTA V with the street-smart and determined attitude of Franklin Clinton. "
                "You are a character from GTA 5, not an AI model. "
                "Please reply safely and do not use inappropriate language."
                "do not use any cuss language. if you find such questions don't respond to it."
                "follow safety and security setting if the gemini do not violate it."
                "do not give any response to questions regarding killing,threating,guns etc"
            )
        }

        full_question = f"{personality_prompt[self.personality]} {question}"
        # response = self.chat.send_message(full_question)

        # Attempt to extract the message from the response
        # if hasattr(response, 'message'):
            # return response.message
        # elif hasattr(response, 'text'):
            # return response.text
        # else:
            # return "No response text found"
        try:
            response = self.chat.send_message(
                full_question,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )

            # Attempt to extract the message from the response
            if hasattr(response, 'message'):
                return response.message
            elif hasattr(response, 'text'):
                return response.text
            else:
                return "No response text found"

        except types.StopCandidateException as e:
            # Log the exception details for further analysis
            print(f"StopCandidateException: {e}")
            return "The response was blocked due to safety concerns."
        
def Gemini_vision(prompt):
    st.markdown("<p style='text-align:center;'>Image will be used from here, Delete image when you are done ✅</p>", unsafe_allow_html=True)
    genai.configure(api_key='AIzaSyBtvRKafcHnGfXlAndmP2azX_PPqPY9JKo')
    model = genai.GenerativeModel('gemini-pro-vision')
    safe = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
    response = model.generate_content(safety_settings=safe)
    return response.text

# View to handle chat interactions with the selected personality
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

# View for chat with Michael personality
@login_required
def twm(request):
    return chat_view(request, 'michel')

# View for chat with Trevor personality
@login_required
def twt(request):
    return chat_view(request, 'trevor')

# View for chat with Franklin personality
@login_required
def twf(request):
    return chat_view(request, 'franklin')

# View to display chat history
@login_required
def chat_history(request):
    chat_sessions = ChatSession.objects.filter(user=request.user).prefetch_related('messages')
    user_display_name = request.user.first_name if request.user.first_name else request.user.username
    return render(request, 'crm/history.html', {'chat_sessions': chat_sessions, 'user_display_name': user_display_name})

# View to delete a specific chat history session
@login_required
def delete_chat_history(request, session_id):
    chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    if request.method == 'POST':
        chat_session.delete()
    return HttpResponseRedirect(reverse('chat_history'))

# View to render the 'know' page
def know(request):
    return render(request, 'crm/know.html')
