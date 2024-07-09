from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')) and not request.user.is_superuser:
            messages.error(request, "You do not have permission to access the admin site.")
            return redirect('home')  # Replace 'home' with the name of your home view
        response = self.get_response(request)
        return response


# middleware.py
from django.utils.deprecation import MiddlewareMixin

class AllowIframeFrom(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'ALLOWALL'
        return response
