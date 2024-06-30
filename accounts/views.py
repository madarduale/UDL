from django.shortcuts import render, redirect
from django.views import  View
from .forms import Signup
from django.contrib import messages
# Create your views here.



class UserSingUpView(View):
    def get(self, request):
        form = Signup()
        return render(request, 'registration/signup.html',{'form':form})
    
    def post(self, request):
        form = Signup(request.POST, None)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'user created successfully!.')
            return redirect('login')
        else:
            messages.error(request, "Please enter valid data!.")
            
        return render(request, 'registration/signup.html',{'form':form})
        
            