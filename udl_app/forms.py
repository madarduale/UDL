from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import(
    Admin, Professor, Student, Course, Lecture, Grade,
    Assignment, AssignmentGrade, AssignmentSubmission,
    Quiz, QuizGrading, QuizSubmission,
    Exam, ExamGrading, ExamSubmission,
    Question, Choice, Resource, EnrolledCourse,
    Discussion, Comment, Profile,
    School, Message, ZoomMeeting,
) 




# class LoginForm(forms.Form):

class BaseUserForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_student', 'is_professor', 'is_admin', 'is_staff', 'is_active']

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['username', 'first_name', 'last_name', 'email', 'is_admin', 'is_student', 'is_professor', 'school']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['school'].queryset = School.objects.filter(name=school)


    
class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['username', 'first_name', 'last_name', 'email', 'is_professor',  'school']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            professeor = Professor.objects.get(username=user)
            for school in professeor.school.all():
                self.fields['school'].queryset = School.objects.filter(name=school)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email',  'is_student', 'UID', 'school']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            student = Student.objects.get(username=user)
            for school in student.school.all():
                self.fields['school'].queryset = School.objects.filter(name=school)
                  
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content', 'url']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title', 'description', 'school', 'professors', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['school'].queryset = School.objects.filter(name=school)
                self.fields['professors'].queryset = Professor.objects.filter(school=school)
            elif user.is_superuser:
                self.fields['school'].queryset = School.objects.all()
                self.fields['professors'].queryset = Professor.objects.all()

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['course', 'title', 'description', 'video']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_professor:
                self.fields['course'].queryset = Course.objects.filter(professors=user)
            elif user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['course'].queryset = Course.objects.filter(school=school)
                # self.fields['course'].queryset = Course.objects.filter(school=admin.school.all())
            elif user.is_superuser:
                self.fields['course'].queryset = Course.objects.all()
        

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'file']
        widgets = {
                'due_date': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_professor:
                self.fields['course'].queryset = Course.objects.filter(professors=user)
            elif user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['course'].queryset = Course.objects.filter(school=school)
                # self.fields['course'].queryset = Course.objects.filter(school=admin.school.all())
            elif user.is_superuser:
                self.fields['course'].queryset = Course.objects.all()
        self.fields['file'].required = False
      

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['assignment', 'student', 'file']

class AssigmmentGradeForm(forms.ModelForm):
    class Meta:
        model = AssignmentGrade
        fields = ['student', 'score','grader', 'feedback', 'assignment']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'title', 'description', 'start_time', 'end_time', 'questions']

class QuizSubmissionForm(forms.ModelForm):
    class Meta:
        model = QuizSubmission
        fields = ['quiz', 'student','answers']

class QuizGradingForm(forms.ModelForm):
    class Meta:
        model = QuizGrading
        fields = ['student', 'score','grader','feedback','submission']
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'title', 'description', 'start_time', 'end_time', 'questions']

class ExamSubmissionForm(forms.ModelForm):
    class Meta:
        model = ExamSubmission
        fields = ['exam', 'student','answers']

class ExamGradingForm(forms.ModelForm):
    class Meta:
        model = ExamGrading
        fields = ['student', 'score','grader','feedback','submission']


class choiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'text', 'is_correct']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['lecture', 'title', 'resource_file']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_professor:
                self.fields['lecture'].queryset = Lecture.objects.filter(course__professors=user)
            elif user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['lecture'].queryset = Lecture.objects.filter(course__school=school)
                # self.fields['course'].queryset = Course.objects.filter(school=admin.school.all())
            elif user.is_superuser:
                self.fields['lecture'].queryset = Lecture.objects.all()

class EnrolledCourseForm(forms.ModelForm):
    class Meta:
        model = EnrolledCourse
        fields = ['course', 'student']

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['course', 'title', 'starter', 'message']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['discussion', 'parent', 'author', 'content', 'likes']

class ZoomMeetingForm(forms.ModelForm):
    class Meta:
        model = ZoomMeeting
        fields = ['course', 'lecture', 'host', 'meeting_id', 'topic', 'start_time', 'duration', 'join_url']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'bio', 'location', 'birth_date', 'telephone']
