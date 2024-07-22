from django.shortcuts import render,redirect
from . forms import CreateUserForm, Loginform
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from google import generativeai as genai
import textwrap



# from razorpay import client
from elevate.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY 
# Create your views here.
# def home(request):
#     return render(request, 'crm/index.html')
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_log")
    context = {'registerform':form}
    return render(request, 'crm/register.html', context=context)
def my_log(request):
    form = Loginform()
    if request.method =="POST":
        form = Loginform(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request,user)
                return redirect("dashboard")
    context = {'loginform':form}
    return render(request, 'crm/my_log.html',context=context)
def user_logout(request):
    auth.logout(request)
    return redirect('home')

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

class ChatSession:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])

    def ask_question(self, question):
        response = self.chat.send_message(question)
        return response

chat_session = ChatSession()
chat_history = []

@csrf_exempt
def home(request):
    global chat_history

    if request.method == 'POST':
        input_text = request.POST.get('input_text')

        if request.POST.get('clear_history'):
            chat_history = [] 
        else:
            response = chat_session.ask_question(input_text)

            chat_history.append({"role": "User", "text": input_text})
            chat_history.append({"role": "Gemini", "text": response.text})

    return render(request, 'crm/index.html', {'chat_history': chat_history})

