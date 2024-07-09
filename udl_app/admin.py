from django.contrib import admin
from .models import(

BaseUser, Profile, Admin, Student, 
Professor, School, Course, EnrolledCourse, 
Lecture, Quiz, QuizGrading, QuizSubmission, 
Question, Exam, ExamGrading, ExamSubmission,
 Assignment, AssignmentGrade, AssignmentSubmission, Grade, 
 Discussion, Message, Resource, Choice, Comment, ZoomMeeting

) 
# Register your models here.


# change the default admin users name to BaseUser in the admin panel 

class BaseUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']


admin.site.register(BaseUser, BaseUserAdmin)



admin.site.register(Profile)
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(School)
admin.site.register(Course)
admin.site.register(EnrolledCourse)
admin.site.register(Lecture)
admin.site.register(Quiz)
admin.site.register(QuizGrading)
admin.site.register(QuizSubmission)
admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(ExamGrading)
admin.site.register(ExamSubmission)
admin.site.register(Assignment)
admin.site.register(AssignmentGrade)
admin.site.register(AssignmentSubmission)
admin.site.register(Grade)
admin.site.register(Discussion)
admin.site.register(Message)
admin.site.register(Resource)
admin.site.register(Choice)
admin.site.register(Comment)
admin.site.register(ZoomMeeting)
