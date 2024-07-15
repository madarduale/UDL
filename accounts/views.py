from django.shortcuts import render, redirect
from django.views import  View
from .forms import AdminSignupForm, StudentSignupForm, ProfessorSignupForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
            user = form.save(commit=False)
            user.save()
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
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
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
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'user created successfully!.')
            return redirect('login')
        else:
            messages.error(request, "Please enter valid data!.")
            
        return render(request, 'registration/professor_signup.html',{'form':form})
           

#login view
class UserLoginView(View):
    def get(self, request):
        # form = UserLoginForm()
        return render(request, 'registration/login.html')
    
    def post(self, request):
        # form = UserLoginForm(data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username',username)
        print('password',password)

        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
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