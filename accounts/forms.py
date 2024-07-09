from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from udl_app.models import Admin, Student, Professor, BaseUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

# class LoginForm(forms.Form):
    
class AdminSignupForm(UserCreationForm):
    class Meta:
        model=Admin
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "is_superuser",
            "is_active",
            "is_staff",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  
        self.fields['email'].help_text = '' 
        self.fields['password1'].help_text = '' 
        self.fields['password2'].help_text = '' 
        self.fields['school'].help_text = '' 
        self.fields['is_superuser'].help_text = '' 
        self.fields['is_active'].help_text = '' 
        self.fields['is_staff'].help_text = '' 
       
class AdminEditForm(UserChangeForm):
    class Meta:
        model=Admin
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "is_superuser",
            "is_active",
            "is_staff",
        ]

class StudentSignupForm(UserCreationForm):
    class Meta:
        model=Student
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "UID",
            "is_student",
            "is_active",

        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  
        self.fields['email'].help_text = '' 
        self.fields['school'].help_text = '' 
        self.fields['UID'].help_text = '' 
        self.fields['password1'].help_text = '' 
        self.fields['password2'].help_text = '' 
        self.fields['is_student'].help_text = '' 
        self.fields['is_active'].help_text = '' 


class StudentEditForm(UserChangeForm):
    class Meta:
        model=Student
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "UID",
            "is_student",
            "is_active",
        ]

class ProfessorSignupForm(UserCreationForm):
    class Meta:
        model=Professor
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "is_professor",
            "is_active",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  
        self.fields['email'].help_text = '' 
        self.fields['school'].help_text = '' 
        self.fields['password1'].help_text = '' 
        self.fields['password2'].help_text = '' 
        self.fields['is_active'].help_text = ''
        self.fields['is_professor'].help_text = ''

class ProfessorEditForm(UserChangeForm):
    class Meta:
        model=Professor
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "is_professor",
            "is_active",
        ]


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  # Hide help text for username field
        self.fields['password'].help_text = ''  # Hide help text for password field



        