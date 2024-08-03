from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')) and not request.user.is_superuser:
            messages.error(request, "You do not have permission to access the admin site.")
            return redirect('dashboard')  
        response = self.get_response(request)
        return response


class AllowIframeFrom(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'ALLOWALL'
        return response



class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_session_key = request.user.current_session_key
            if current_session_key and current_session_key != request.session.session_key:
                messages.error(request, 'You login another browser or device')
                logout(request)
        response = self.get_response(request)
        return response
