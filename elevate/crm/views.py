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

def send_email(request):
    send_email_to_clients()
    return redirect('/')

# from razorpay import client
from elevate.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY 
# Create your views here.
# def home(request):
#     return render(request, 'crm/index.html')


# def register(request):
#     form = CreateUserForm()
#     if request.method == "POST":
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("my_log")
#     context = {'registerform':form}
#     return render(request, 'crm/register.html', context=context)

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
    return redirect('welcome')


# @login_required(login_url="")
client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY ))
def dashboard(request):
    # if request.method=='POST':
    #     amount = 500
    #     order_currency = 'INR'
    #     client = razorpay.Client(auth=("rzp_live_2DWZBQ5mIimbcX", "jy8T9rW0uIhp25NXxy67IhVE"))
    #     data = { "amount": amount, "currency":order_currency, 'payment_capture':'1' }
    #     payment = client.order.create(data=data)
    order_amount = 50000
    order_currency = 'INR'
    payment_order = client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture=1))
    payment_order_id = payment_order['id']
    context = {
        'amount':500, 'api_key':RAZORPAY_API_KEY, 'order_id':payment_order_id
    }

    return render(request,'crm/dash.html',context)

genai.configure(api_key="AIzaSyBtvRKafcHnGfXlAndmP2azX_PPqPY9JKo")

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

class ChatSessionm:
    def __init__(self, personality):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.personality = personality

    def ask_question(self, question):
        # Customize the prompt based on the personality
        personality_prompt = {
            'michel': "You are Michel from GTA V, a balanced and rational character.",
            # 'trevor': "You are Trevor from GTA V, known for bank robbery and a criminal.",
            # 'franklin': "You are Franklin from GTA V, a clever and street-smart individual."
        }

        full_question = f"{personality_prompt[self.personality]} {question}"
        response = self.chat.send_message(full_question)
        return response
current_chat_session = None
chat_history = []


class ChatSessionf:
    def __init__(self, personality):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.personality = personality

    def ask_question(self, question):
        # Customize the prompt based on the personality
        personality_prompt = {
            # 'michel': "You are Michel from GTA V, a balanced and rational character.",
            # 'trevor': "You are Trevor from GTA V, known for bank robbery and a criminal.",
            'franklin': "You are Franklin from GTA V, a clever and street-smart individual."
        }

        full_question = f"{personality_prompt[self.personality]} {question}"
        response = self.chat.send_message(full_question)
        return response
current_chat_session = None
chat_history = []



class ChatSessiont:
    def __init__(self, personality):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.personality = personality

    def ask_question(self, question):
        # Customize the prompt based on the personality
        personality_prompt = {
            # 'michel': "You are Michel from GTA V, a balanced and rational character.",
            'trevor': "You are Trevor from GTA V, known for bank robbery and a criminal.",
            # 'franklin': "You are Franklin from GTA V, a clever and street-smart individual."
        }

        full_question = f"{personality_prompt[self.personality]} {question}"
        response = self.chat.send_message(full_question)
        return response


current_chat_session = None
chat_history = []

# @csrf_exempt
# @csrf_protect
# def index(request):
#     global chat_history, current_chat_session

#     if request.method == 'POST':
#         input_text = request.POST.get('input_text')
#         selected_personality = request.POST.get('personality','michel')  # Default personality

        # if request.POST.get('clear_history'):
        #     chat_history = [] 
        #     current_chat_session = None
        # else:
        #     if not current_chat_session or current_chat_session.personality != selected_personality:
        #         current_chat_session = ChatSession(selected_personality)

        #     response = current_chat_session.ask_question(input_text)

        #     chat_history.append({"role": "Sen", "text": input_text})
        #     chat_history.append({"role": selected_personality.capitalize(), "text": response.text})
    #     if not current_chat_session or current_chat_session.personality != selected_personality:
    #         chat_history = []
    #         current_chat_session = ChatSession(selected_personality)

    #     response = current_chat_session.ask_question(input_text)

    #     chat_history.append({"role": "User", "text": input_text})
    #     chat_history.append({"role": selected_personality.capitalize(), "text": response.text})


    # return render(request, 'crm/index.html', {
    #     'chat_history': chat_history,
    #     'current_personality': current_chat_session.personality if current_chat_session else 'michel'
    # })

def welcome(request):
    if request.method == 'POST':
        selected_personality = request.POST.get('personality','michel')
    return render(request,'crm/welcome.html')

@csrf_protect
def twt(request):
    global chat_history, current_chat_session

    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        selected_personality = request.POST.get('personality','trevor')  # Default personality

        # if request.POST.get('clear_history'):
        #     chat_history = [] 
        #     current_chat_session = None
        # else:
        #     if not current_chat_session or current_chat_session.personality != selected_personality:
        #         current_chat_session = ChatSession(selected_personality)

        #     response = current_chat_session.ask_question(input_text)

        #     chat_history.append({"role": "Sen", "text": input_text})
        #     chat_history.append({"role": selected_personality.capitalize(), "text": response.text})
        if not current_chat_session or current_chat_session.personality != selected_personality:
            chat_history = []
            current_chat_session = ChatSessiont(selected_personality)

        response = current_chat_session.ask_question(input_text)

        chat_history.append({"role": "User", "text": input_text})
        chat_history.append({"role": selected_personality.capitalize(), "text": response.text})
        
    return render(request, 'crm/twt.html', {
        'chat_history': chat_history,
        'current_personality': current_chat_session.personality if current_chat_session else 'michel'
    })

@csrf_protect
def twm(request):
    global chat_history, current_chat_session

    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        selected_personality = request.POST.get('personality','michel')  # Default personality

        # if request.POST.get('clear_history'):
        #     chat_history = [] 
        #     current_chat_session = None
        # else:
        #     if not current_chat_session or current_chat_session.personality != selected_personality:
        #         current_chat_session = ChatSession(selected_personality)

        #     response = current_chat_session.ask_question(input_text)

        #     chat_history.append({"role": "Sen", "text": input_text})
        #     chat_history.append({"role": selected_personality.capitalize(), "text": response.text})
        if not current_chat_session or current_chat_session.personality != selected_personality:
            chat_history = []
            current_chat_session = ChatSessionm(selected_personality)

        response = current_chat_session.ask_question(input_text)

        chat_history.append({"role": "User", "text": input_text})
        chat_history.append({"role": selected_personality.capitalize(), "text": response.text})
        
    return render(request, 'crm/twm.html', {
        'chat_history': chat_history,
        'current_personality': current_chat_session.personality if current_chat_session else 'michel'
    })


@csrf_protect
def twf(request):
    global chat_history, current_chat_session

    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        selected_personality = request.POST.get('personality','franklin')  # Default personality

        # if request.POST.get('clear_history'):
        #     chat_history = [] 
        #     current_chat_session = None
        # else:
        #     if not current_chat_session or current_chat_session.personality != selected_personality:
        #         current_chat_session = ChatSession(selected_personality)

        #     response = current_chat_session.ask_question(input_text)

        #     chat_history.append({"role": "Sen", "text": input_text})
        #     chat_history.append({"role": selected_personality.capitalize(), "text": response.text})
        if not current_chat_session or current_chat_session.personality != selected_personality:
            chat_history = []
            current_chat_session = ChatSessionf(selected_personality)

        response = current_chat_session.ask_question(input_text)

        chat_history.append({"role": "User", "text": input_text})
        chat_history.append({"role": selected_personality.capitalize(), "text": response.text})
        
    return render(request, 'crm/twf.html', {
        'chat_history': chat_history,
        'current_personality': current_chat_session.personality if current_chat_session else 'michel'
    })

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


# aa junu che...uncomment aan ekarvanu che
# class GoogleLoginView(View):
#     def get(self, request, *args, **kwargs):
#         provider = 'google'
#         client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
#         redirect_uri = request.build_absolute_uri('http://127.0.0.1:8000/index')
#         scope = " ".join(settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE'])
#         auth_params = "&".join(f"{k}={v}" for k, v in settings.SOCIALACCOUNT_PROVIDERS['google']['AUTH_PARAMS'].items())

#         google_auth_url = (f"https://accounts.google.com/o/oauth2/auth?"
#                            f"client_id={client_id}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&{auth_params}")

#         # google_auth_url = http://127.0.0.1:8000/index
        
#         return redirect(google_auth_url)

from django.conf import settings
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

class GoogleLoginView(View):
    def get(self, request, *args, **kwargs):
        client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
        redirect_uri = request.build_absolute_uri(reverse('google_callback'))
        scope = " ".join(settings.SOCIALACCOUNT_PROVIDERS['google']['SCOPE'])
        auth_params = "&".join(f"{k}={v}" for k, v in settings.SOCIALACCOUNT_PROVIDERS['google']['AUTH_PARAMS'].items())

        google_auth_url = (f"https://accounts.google.com/o/oauth2/auth?"
                           f"client_id={client_id}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&{auth_params}")

        return redirect(google_auth_url)


import requests
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.conf import settings
from django.contrib.auth.models import User

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

        user_id = user_info['id']
        user_name = user_info['name']
        user_email = user_info['email']

        # Save user info to database
        self.save_user_to_db(user_id, user_name, user_email)

        # Redirect to /index after successful login
        return redirect('/index')

    def save_user_to_db(self, user_id, user_name, user_email):
        user, created = User.objects.get_or_create(username=user_id, defaults={'first_name': user_name, 'email': user_email})
        if not created:
            user.first_name = user_name
            user.email = user_email
            user.save()

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login as auth_login

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('/index')
#     if request.method == 'POST':
#         # Handle login form submission
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             # Log the user in
#             auth_login(request, form.get_user())
#             return redirect('/index')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'home.html', {'loginform': form})
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

    response = render(request, 'home.html', {'loginform': form})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1.
    response['Pragma'] = 'no-cache'  # HTTP 1.0.
    response['Expires'] = '0'  # Proxies.
    return response



# class GoogleLoginView(RedirectView):
#     def get_redirect_url(self, *args, **kwargs):
#         return self.request.build_absolute_uri('/accounts/google/login/')