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
                return redirect('index')
    context = {'loginform':form}
    return render(request, 'crm/home.html',context=context)
def user_logout(request):
    user_logout(request)
    return redirect('/')


# @login_required(login_url="my_log")
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