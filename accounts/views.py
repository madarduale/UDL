from django.contrib.auth.models import Group
#import letters and numbers for password generation
import random
import string
from django.shortcuts import render, redirect
from django.views import  View
from .forms import AdminSignupForm, StudentSignupForm, ProfessorSignupForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from udl_app.models import Admin, Student, Professor
# Create your views here.



#Admin signup view
class AdminSingUpView(View):
    def get(self, request):
        form = AdminSignupForm()
        return render(request, 'registration/admin_signup.html',{'form':form})
    
    def post(self, request):
        form = AdminSignupForm(request.POST, None)
        if form.is_valid():
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            school = form.cleaned_data.get('school')
            if school is not None:
                user.school.set(list(school))

            admin_group = Group.objects.get(name='Admins')
            admin_group.user_set.add(user)
            send_welcome_email(user, password)
            messages.success(request, 'user created successfully!.')
            return redirect('login')
        else:
            messages.error(request, "Please enter valid data!.")
            
        return render(request, 'registration/admin_signup.html',{'form':form})
        

#Student signup view
class StudentSingUpView(View):
    def get(self, request):
        form = StudentSignupForm(user=request.user)
        return render(request, 'registration/student_signup.html',{'form':form})
    
    def post(self, request):
        form = StudentSignupForm(request.POST, None, user=request.user)
        #get returned error messages
        # error = form.errors
        # print('error',error)
        if form.is_valid():
            #Generate a random password for the user
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            school = form.cleaned_data.get('school')
            if school is not None:
                user.school.set(list(school))

            student_group = Group.objects.get(name='Students')
            student_group.user_set.add(user)
            send_welcome_email(user, password)
            messages.success(request, 'user created successfully!.')
            return redirect('login')
        else:
            messages.error(request, "Please enter valid data!.")
            
        return render(request, 'registration/student_signup.html',{'form':form})
    

    
#Professor signup view
class ProfessorSingUpView(View):
    def get(self, request):
        form = ProfessorSignupForm(user=request.user)
        return render(request, 'registration/professor_signup.html',{'form':form})
    
    def post(self, request):
        form = ProfessorSignupForm(request.POST, None, user=request.user)
        if form.is_valid():
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            school = form.cleaned_data.get('school')
            if school is not None:
                user.school.set(list(school))
            
            professor_group = Group.objects.get(name='Professors')
            professor_group.user_set.add(user)
            send_welcome_email(user, password)
            messages.success(request, 'user created successfully!.')
            return redirect('login')
        else:
            messages.error(request, "Please enter valid data!.")
            
        return render(request, 'registration/professor_signup.html',{'form':form})
           

def send_welcome_email(user, password, **kwargs):
    subject = 'Welcome to University Digital Learning'
    message = f"Dear {user.first_name},\n\n" \
        f"Your account has been successfully created.\n" \
        f"Here are your login details:\n\n" \
        f"Username: {user.username}\n" \
        f"Password: {password}\n\n" \
        f"Please login to your account to access the learning materials.\n\n" \
        f"Best regards,\nUniversity Digital Learning Team"
    recipient_list = [user.email]
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

#login view
class UserLoginView(View):
    def get(self, request):
        # form = UserLoginForm()
        return render(request, 'registration/login.html')
    
    def post(self, request):
        # form = UserLoginForm(data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user.current_session_key = request.session.session_key
                user.save()
                messages.success(request, 'Login successful.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        except:
            messages.error(request, 'Invalid username or password.')
        return render(request, 'registration/login.html')
    

        # if form.is_valid():
        #     username = form.cleaned_data.get('username')
        #     password = form.cleaned_data.get('password')
        #     print('username',username)
        #     print('password',password)
        #     user = authenticate(username=username, password=password)
        #     if user is not None:
        #         login(request, user)
        #         messages.success(request, 'Login successful.')
        #         return redirect('home')
        #     else:
        #         messages.error(request, 'Invalid username or password.')
        # else:
        #     messages.error(request, 'Invalid username or password.')
        # return render(request, 'registration/login.html',{'form':form})
    

    # Logout view
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')
    
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')