from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from django.db.models import Q
from .models import(
    BaseUser, Admin, Professor, Student, Course, Lecture, Grade,
    Assignment, AssignmentGrade, AssignmentSubmission,
    Exam, ExamGrading, ExamSubmission,
    Question, Choice, Resource, EnrolledCourse,
    Discussion, Comment, Profile, Semester,
    School, Message, ZoomMeeting,
) 

User = get_user_model()



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
    courses = forms.ModelMultipleChoiceField(
    queryset=Course.objects.none(),  # Start with an empty queryset
    required=False,
    widget=forms.CheckboxSelectMultiple  # Use a checkbox widget for multiple selection
    )
    class Meta:
        model = Professor
        fields = ['username', 'first_name', 'last_name', 'email', 'is_professor',  'school']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            professor = Professor.objects.get(username=user)
            # for school in professeor.school.all():
            #     self.fields['school'].queryset = School.objects.filter(name=school)
            self.fields['school'].queryset = professor.school.all()  # Filter schools for the professor
            self.fields['courses'].queryset = Course.objects.filter(professors=professor)  # Filter courses for the professor


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
        fields = ['name', 'semesters']



# class MessageForm(forms.ModelForm):
#     recipients = forms.ModelMultipleChoiceField(queryset=User.objects.none(), widget=forms.CheckboxSelectMultiple)

#     class Meta:
#         model = Message
#         fields = ['recipients', 'subject', 'content', 'url']

#     def __init__(self, *args, **kwargs):
#         request = kwargs.pop('request', None)
#         super(MessageForm, self).__init__(*args, **kwargs)
        
#         if request:
#             if request.user.is_superuser:
#                 self.fields['recipients'].queryset = User.objects.all()
                
#             elif request.user.is_admin:
#                 admin = Admin.objects.get(id=request.user.id)
#                 school = admin.school.first()  
#                 if school:
#                     self.fields['recipients'].queryset = User.objects.filter(student__school=school) | \
#                                                         User.objects.filter(professor__school=school)
#                 else:
#                     self.fields['recipients'].queryset = User.objects.none()
            
#             elif request.user.is_professor:
#                 professor = Professor.objects.get(id=request.user.id)
#                 courses_taught = professor.courses_taught.all()
#                 self.fields['recipients'].queryset = Student.objects.filter(enrolled_student__course__in=courses_taught).distinct()
            
#             elif request.user.is_student:
#                 student = Student.objects.get(id=request.user.id)
#                 courses = student.enrolled_student.all()
#                 school = student.school.first() 
#                 schools = student.school.all() 
#                 enrolled_courses = EnrolledCourse.objects.filter(student=student)
#                 courses = Course.objects.filter(enrolled_course__in=enrolled_courses)
#                 professors = Professor.objects.filter(courses_taught__in=courses)
#                 admins = Admin.objects.filter(school__in=schools)
#                 self.fields['recipients'].queryset = BaseUser.objects.filter(Q(professor__in=professors) | Q(admin__in=admins))
#                 # courses = Course.objects.filter(enrolled_course=enrolled_courses.first())
#                 # if school:
#                 #     for course in courses:
#                 #         self.fields['recipients'].queryset = Professor.objects.filter(courses_taught=course).union(Admin.objects.filter(school=school))
#                 #     # self.fields['recipients'].queryset = Professor.objects.filter(courses_taught__in=course) | \
#                 #     #                                     Admin.objects.filter(admin__school=school)
#                 # else:
#                 #     self.fields['recipients'].queryset = User.objects.none()

class MessageForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    professors = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    admins = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Message
        fields = ['subject', 'content', 'url']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        
        if request:
            student_group = Group.objects.get(name='Students')
            professor_group = Group.objects.get(name='Professors')
            admin_group = Group.objects.get(name='Admins')

            if request.user.is_superuser:
                self.fields['students'].queryset = User.objects.filter(groups=student_group)
                self.fields['professors'].queryset = User.objects.filter(groups=professor_group)
                self.fields['admins'].queryset = User.objects.filter(groups=admin_group)

            elif request.user.is_admin:
                admin = Admin.objects.get(id=request.user.id)
                school = admin.school.first()  
                if school:
                    self.fields['students'].queryset = User.objects.filter(student__school=school)
                    self.fields['professors'].queryset = User.objects.filter(professor__school=school)
                else:
                    self.fields['students'].queryset = User.objects.none()
                    self.fields['professors'].queryset = User.objects.none()

            elif request.user.is_professor:
                professor = Professor.objects.get(id=request.user.id)
                courses_taught = professor.courses_taught.all()
                self.fields['students'].queryset = User.objects.filter(groups=student_group, student__enrolled_student__course__in=courses_taught).distinct()
                self.fields['admins'].queryset = User.objects.filter(groups=admin_group, admin__school=professor.school.first())
            
            elif request.user.is_student:
                student = Student.objects.get(id=request.user.id)
                schools = student.school.all() 
                enrolled_courses = EnrolledCourse.objects.filter(student=student)
                courses = Course.objects.filter(enrolled_course__in=enrolled_courses)
                self.fields['professors'].queryset = User.objects.filter(groups=professor_group, professor__courses_taught__in=courses).distinct()
                self.fields['admins'].queryset = User.objects.filter(groups=admin_group, admin__school__in=schools).distinct()
        if self.instance.pk:
            self.fields['students'].initial = self.instance.recipients.filter(groups__name='Students')
            self.fields['professors'].initial = self.instance.recipients.filter(groups__name='Professors')
            self.fields['admins'].initial = self.instance.recipients.filter(groups__name='Admins')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title', 'description', 'school', 'professors', 'semester', 'image']

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

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['semester', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date', 'format': '%d/%m/%Y'}),
            'end_date': forms.DateInput(attrs={'type':'date', 'format': '%d/%m/%Y'})
        }

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_student:
                enrolled_courses = EnrolledCourse.objects.filter(student=user)
                assignments = Assignment.objects.filter(course__in=enrolled_courses.values_list('course', flat=True))
                valid_assignments = []
                for assignment in assignments:
                    if assignment.due_date >= timezone.now():
                        valid_assignments.append(assignment)
                self.fields['assignment'].queryset = Assignment.objects.filter(id__in=[assignment.id for assignment in valid_assignments])
                self.fields['student'].queryset = Student.objects.filter(username=user)
            elif user.is_professor:
                self.fields['assignment'].queryset = Assignment.objects.filter(course__professors=user) 
                courses_taught = Course.objects.filter(professors=user)
                enrolled_students = Student.objects.filter(enrolled_student__course__in=courses_taught).distinct()
                self.fields['student'].queryset = enrolled_students
            elif user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['assignment'].queryset = Assignment.objects.filter(course__school=school)
                    self.fields['student'].queryset = Student.objects.filter(school=school)
            elif user.is_superuser:
                self.fields['assignment'].queryset = Assignment.objects.all()
        self.fields['file'].required = False

class AssigmmentGradeForm(forms.ModelForm):
    class Meta:
        model = AssignmentGrade
        fields = ['student', 'score','grader', 'feedback', 'assignment_solution']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_professor:
                course = Course.objects.filter(professors=user)
                self.fields['assignment_solution'].queryset = AssignmentSubmission.objects.filter(assignment__course__in=course)
                course = Course.objects.filter(professors=user)
                self.fields['student'].queryset = Student.objects.filter(enrolled_student__course__in=course).distinct()
                self.fields['grader'].queryset = Professor.objects.filter(username=user)
            elif user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['assignment_solution'].queryset = AssignmentSubmission.objects.filter(assignment__course__school=school)
                    self.fields['student'].queryset = Student.objects.filter(school=school)
                    self.fields['grader'].queryset = Professor.objects.filter(school=school)
            elif user.is_superuser:
                self.fields['assignment_solution'].queryset = Assignment.objects.all()

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['course', 'question', 'marks', 'question_type']

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
            elif user.is_superuser:
                self.fields['course'].queryset = Course.objects.all()

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'title', 'start_time', 'end_time', 'description', 'exam_type',  'questions']
        widgets = {
                'start_time': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
                'end_time': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_professor:
                self.fields['course'].queryset = Course.objects.filter(professors=user)
                self.fields['questions'].queryset = Question.objects.filter(course__professors=user)
            elif user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['course'].queryset = Course.objects.filter(school=school)
                    self.fields['questions'].queryset = Question.objects.filter(course__school=school)
            elif user.is_superuser:
                self.fields['course'].queryset = Course.objects.all()

class ExamSubmissionForm(forms.ModelForm):
    class Meta:
        model = ExamSubmission
        fields = ['exam', 'student','answers']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_student:
                enrolled_courses = EnrolledCourse.objects.filter(student=user)
                exams = Exam.objects.filter(course__in=enrolled_courses.values_list('course', flat=True))
                valid_exams = []
                for exam in exams:
                    if exam.end_time >= timezone.now():
                        valid_exams.append(exam)
                self.fields['exam'].queryset = Exam.objects.filter(id__in=[exam.id for exam in valid_exams])
                self.fields['student'].queryset = Student.objects.filter(username=user)
            elif user.is_professor:
                self.fields['exam'].queryset = Exam.objects.filter(course__professors=user) 
                courses_taught = Course.objects.filter(professors=user)
                enrolled_students = Student.objects.filter(enrolled_student__course__in=courses_taught).distinct()
                self.fields['student'].queryset = enrolled_students
            elif user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['exam'].queryset = Exam.objects.filter(course__school=school)
                    self.fields['student'].queryset = Student.objects.filter(school=school)
            elif user.is_superuser:
                self.fields['exam'].queryset = Exam.objects.all()

class ExamGradingForm(forms.ModelForm):
    class Meta:
        model = ExamGrading
        fields = ['student', 'score','grader','feedback','submission']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_professor:
                course = Course.objects.filter(professors=user)
                self.fields['submission'].queryset = ExamSubmission.objects.filter(exam__course__in=course)
                course = Course.objects.filter(professors=user)
                self.fields['student'].queryset = Student.objects.filter(enrolled_student__course__in=course).distinct()
                self.fields['grader'].queryset = Professor.objects.filter(username=user)
            elif user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['submission'].queryset = ExamSubmission.objects.filter(exam__course__school=school)
                    self.fields['student'].queryset = Student.objects.filter(school=school)
                    self.fields['grader'].queryset = Professor.objects.filter(school=school)
            elif user.is_superuser:
                self.fields['submission'].queryset = Exam.objects.all()


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'choice', 'correct_choice']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            if user.is_professor:
                self.fields['question'].queryset = Question.objects.filter(course__professors=user)
            elif user.is_admin:
                admin = Admin.objects.get(username=user)
                for school in admin.school.all():
                    self.fields['question'].queryset = Question.objects.filter(course__school=school)
            elif user.is_superuser:
                self.fields['question'].queryset = Question.objects.all()
        if question is not None:
            self.fields['question'].queryset = Question.objects.filter(id=question.id)

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
        fields = [ 'title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ZoomMeetingForm(forms.ModelForm):
    class Meta:
        model = ZoomMeeting
        fields = ['course', 'lecture', 'host', 'meeting_id', 'topic', 'start_time', 'duration', 'join_url']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'bio', 'location', 'birth_date', 'telephone']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type':'date', 'format': '%d/%m/%Y'}),
            'telephone': forms.TextInput(attrs={'placeholder': 'e.g. +25263xxxxxxx'}),
        }
