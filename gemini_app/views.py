from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from google import generativeai as genai
import textwrap

genai.configure(api_key="Your Gemini Api Key ")

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
def index(request):
    global chat_history

    if request.method == 'POST':
        input_text = request.POST.get('input_text')

        if request.POST.get('clear_history'):
            chat_history = [] 
        else:
            response = chat_session.ask_question(input_text)

            chat_history.append({"role": "Sen", "text": input_text})
            chat_history.append({"role": "Gemini", "text": response.text})

    return render(request, 'gemini_app/index.html', {'chat_history': chat_history})
