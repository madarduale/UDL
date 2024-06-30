from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from udl_app.models import BaseUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

# class LoginForm(forms.Form):
    
class Signup(UserCreationForm):
    class Meta:
        model=BaseUser
        fields = [
            "username",
            # "password1",
            # "password2",
            "first_name",
            "last_name",
            "email",
            # "is_professor",
            "is_superuser",
            # "is_student",
            "is_active",
            "is_staff",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  # Hide help text for username field
        self.fields['email'].help_text = '' 
        self.fields['password1'].help_text = '' 
        self.fields['password2'].help_text = '' 
        # self.fields['is_professor'].help_text = '' 
        self.fields['is_superuser'].help_text = '' 
        self.fields['is_active'].help_text = '' 
        # self.fields['is_student'].help_text = '' 
        self.fields['is_staff'].help_text = '' 
        # self.fields['email'].help_text = '' 
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.layout = Layout(
    #         Row(
    #             Column('username', css_class='form-group col-md-6 mb-0'),
    #             Column('email', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         # Row(
    #         #     Column('password1', css_class='form-group col-md-6 mb-0'),
    #         #     Column('password2', css_class='form-group col-md-6 mb-0'),
    #         #     css_class='form-row'
    #         # ),
    #         'is_professor',
    #         'first_name',
    #         'last_name',
    #         'is_superuser',
    #         'is_student',
    #         'is_active',
    #         'is_staff',
    #         Submit('submit', 'Sign up')
    #     )

class UserEdit(UserChangeForm):
    class Meta:
        model=BaseUser
        fields = [
            "username",
            # "password1",
            # "password2",
            # "is_professor",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            # "is_student",
            "is_active",
            "is_staff",
        ]






        