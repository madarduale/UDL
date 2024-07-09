
from django.urls import path, include
from .views import (
    AdminSingUpView,
    StudentSingUpView,
    ProfessorSingUpView,
    UserLoginView,
    UserLogoutView
)
urlpatterns = [
  path('admin/signup/', AdminSingUpView.as_view(), name='admin_signup'),
  path('student/signup/', StudentSingUpView.as_view(), name='student_signup'),
  path('professor/signup/', ProfessorSingUpView.as_view(), name='professor_signup'),
  path('login/', UserLoginView.as_view(), name='login'),
  path('logout/', UserLogoutView.as_view(), name='logout'),
]
