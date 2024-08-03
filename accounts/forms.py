from django import forms
import random
import string
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from udl_app.models import Admin, Student, Professor, BaseUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from udl_app.models import School

# class LoginForm(forms.Form):
    
class AdminSignupForm(forms.ModelForm):
    class Meta:
        model=Admin
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "is_active",
            "is_admin"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  
        self.fields['email'].help_text = '' 
        # self.fields['password1'].help_text = '' 
        # self.fields['password2'].help_text = '' 
        self.fields['school'].help_text = '' 
        self.fields['is_admin'].help_text = '' 
        self.fields['is_active'].help_text = '' 
 
       
class AdminEditForm(UserChangeForm):
    class Meta:
        model=Admin
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "school",
            "is_admin",
            "is_active",
            # "is_staff",
        ]

class StudentSignupForm(forms.ModelForm):
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
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  
        self.fields['email'].help_text = '' 
        self.fields['school'].help_text = '' 
        self.fields['UID'].help_text = '' 
        # self.fields['password2'].help_text = '' 
        self.fields['is_student'].help_text = '' 
        self.fields['is_active'].help_text = '' 

        if user.is_superuser:
            self.fields['school'].queryset = School.objects.all()
        elif user.is_admin:
            admin = Admin.objects.get(username=user)
            self.fields['school'].queryset = School.objects.filter(admin_school=admin)
    
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  
        self.fields['email'].help_text = '' 
        self.fields['school'].help_text = '' 
        self.fields['UID'].help_text = '' 
        self.fields['is_student'].help_text = '' 
        self.fields['is_active'].help_text = '' 

        if user.is_superuser:
            self.fields['school'].queryset = School.objects.all()
        elif user.is_admin:
            admin = Admin.objects.get(username=user)
            self.fields['school'].queryset = School.objects.filter(admin_school=admin)

class ProfessorSignupForm(forms.ModelForm):
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
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  
        self.fields['email'].help_text = '' 
        self.fields['school'].help_text = '' 
        # self.fields['password1'].help_text = '' 
        # self.fields['password2'].help_text = '' 
        self.fields['is_active'].help_text = ''
        self.fields['is_professor'].help_text = ''

        if user.is_superuser:
            self.fields['school'].queryset = School.objects.all()
        elif user.is_admin:
            admin = Admin.objects.get(username=user)
            self.fields['school'].queryset = School.objects.filter(admin_school=admin)
        

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  
        self.fields['email'].help_text = '' 
        self.fields['school'].help_text = '' 
        self.fields['is_professor'].help_text = '' 
        self.fields['is_active'].help_text = '' 

        if user.is_superuser:
            self.fields['school'].queryset = School.objects.all()
        elif user.is_admin:
            admin = Admin.objects.get(username=user)
            self.fields['school'].queryset = School.objects.filter(admin_school=admin)


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  # Hide help text for username field
        self.fields['password'].help_text = ''  # Hide help text for password field



        