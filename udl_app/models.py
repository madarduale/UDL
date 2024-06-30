from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
# Create your models here.


class BaseUser(AbstractUser):
    # is_professor = models.BooleanField(default=False)
    # is_student = models.BooleanField(default=False)
      # making email unique and required
    email = models.EmailField(_('email address'), unique=True)

    # making first_name and last_name are required
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)

class School(models.Model):
    name = models.CharField(max_length=100)


class Admin(BaseUser):
    school = models.ManyToManyField(School, related_name='admin_school')

class Professor(BaseUser):
    school = models.ManyToManyField(School, related_name='proffesor_school')

class Student(BaseUser):
    school = models.ManyToManyField(School, related_name='student_school')
    UID = models.CharField(max_length=250, unique=True)

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses_school')
    professors = models.ManyToManyField(Professor, related_name='courses_taught')
    # students = models.ManyToManyField(User, related_name='courses_enrolled')

    def __str__(self):
        return f"{self.title} ({self.code})"


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    file = models.FileField(upload_to='assigments/', blank=True, null=True)

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submitted_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment.title}"

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    questions = models.ManyToManyField('Question', related_name='quizzes')

    def __str__(self):
        return self.title

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    questions = models.ManyToManyField('Question', related_name='exams')


    def __str__(self):
        return self.title
    

class QuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username}'s submission for {self.quiz.title}"

class ExamSubmission(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username}'s submission for {self.exam.title}"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    score = models.FloatField(default=0)
    grader = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)
    graded_at = models.DateTimeField(auto_now_add=True, blank=True)
    feedback = models.TextField(blank=True)

class QuizGrading(Grade):
    submission = models.OneToOneField(QuizSubmission, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f"Grading for {self.submission.student.username}'s Quiz {self.submission.quiz.title}"

class ExamGrading(Grade):
    submission = models.OneToOneField(ExamSubmission, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f"Grading for {self.submission.student.username}'s Exam {self.submission.exam.title}"

# class QuizGrade(Grade):
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.student.username}'s grade for {self.quiz.title}"


# class ExamGrade(Grade):
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.student.username}'s grade for {self.exam.title}"


class AssignmentGrade(Grade):
    assignment = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.student.username}'s grade for {self.assignment.title}"


class Question(models.Model):
    text = models.TextField()
    # quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    # exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
        ('LA', 'Long Answer'),
    ]
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES, default='MCQ')

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    resource_file = models.FileField(upload_to='resources/')

    def __str__(self):
        return self.title
    

class EnrolledCourse(models.Model):
    course = models.ManyToManyField(Course, related_name='enrolled_course')
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='enrolled_student')


class Discussion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=255)
    starter = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='discussions_started')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.starter.username}"


class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    author = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(BaseUser, related_name='liked_comments', blank=True)

    def __str__(self):
        return f"{self.author.username} in {self.discussion.title}"
    

class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=Admin)
def create_admin_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Admin)
def save_admin_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Professor)
def create_professor_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Professor)
def save_professor_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Student)
def save_student_profile(sender, instance, **kwargs):
    instance.profile.save()

# signal that remind the student if there is message, zoom meeting, quiz, exam, assigment, or assigment expired date is near.


class ZoomMeeting(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE, null=True, blank=True)
    host = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='zoom_meetings')
    meeting_id = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    join_url = models.URLField()

    def __str__(self):
        return f"{self.topic} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Message(models.Model):
    sender = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='sended_messages')
    recipient = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=100)
    content = models.TextField()
    url = models.URLField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    

# class MessageFromStudent(models.Model):
#     sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sended_messages')
#     recipient = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='received_messages')
#     subject = models.CharField(max_length=100)
#     content = models.TextField()
#     url = models.URLField(max_length=200, blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.subject