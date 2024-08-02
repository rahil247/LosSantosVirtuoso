
# Importing necessary classes and modules from Django for form handling and user authentication.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import ChatSession, Message, Contact


# Creating a custom user creation form based on Django's built-in UserCreationForm.
# This form is used to register a new user with additional customizations.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # Specifying the model to use for this form, which is the built-in User model.
        model = User
        # Defining the fields to include in the form.
        fields = ('username', 'email', 'password1', 'password2')
        # Customizing the widgets for each field to add placeholders.
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }
        # Removing labels from the form fields.
        labels = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
        # Removing help texts from the form fields.
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

# Creating a custom login form based on Django's built-in AuthenticationForm.
# This form is used to authenticate a user during login with additional customizations.
class Loginform(AuthenticationForm):
    # Customizing the username field to add CSS classes and a placeholder.
    username = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    # Customizing the password field to add CSS classes and a placeholder.
    password = forms.CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


# Creating a form for the ChatSession model.
# This form is used to handle the creation and updating of chat sessions.
class Mes(forms.ModelForm):
    class Meta:
        # Specifying the model to use for this form, which is the ChatSession model.
        model = ChatSession
        # Defining the fields to include in the form.
        fields = ['user', 'personality']

# Creating a form for the Message model.
# This form is used to handle the creation and updating of messages within a chat session.
class Messagq(forms.ModelForm):
    class Meta:
        # Specifying the model to use for this form, which is the Message model.
        model = Message
        # Defining the fields to include in the form.
        fields = ['chat_session', 'role', 'text']

# Creating a form for the Contact model.
# This form is used to handle the creation and updating of contact information.
class ContactForm(forms.ModelForm):
    class Meta:
        # Specifying the model to use for this form, which is the Contact model.
        model = Contact
        # Defining the fields to include in the form.
        fields = ['name', 'email', 'message']
