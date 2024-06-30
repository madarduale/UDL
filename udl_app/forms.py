from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Message


# class LoginForm(forms.Form):
    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content', 'url']