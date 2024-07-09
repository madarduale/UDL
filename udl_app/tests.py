from django.test import TestCase
from django.urls import reverse
# from django.contrib.auth.models import User
from .models import Course, Lecture, Assignment, Question, Profile, School, BaseUser

class LectureModelTest(TestCase):

    def setUp(self):
        self.school = School.objects.create(
            name="Test School",
        )
        self.course = Course.objects.create(
            code="CS101",
            title="Introduction to Computer Science",
            description="A basic course on computer science",
            school=self.school,
        )
        self.lecture = Lecture.objects.create(
            course=self.course,
            title="Lecture 1",
            description="Introduction to the course",
            date="2024-07-05 10:00:00",
            video_url="http://example.com/video",
        )

    def test_lecture_creation(self):
        self.assertEqual(self.lecture.title, "Lecture 1")
        self.assertEqual(self.lecture.course, self.course)
        self.assertEqual(str(self.lecture), "Lecture 1")

class AssignmentModelTest(TestCase):

    def setUp(self):
        self.school = School.objects.create(
            name="Test School",
        )
        self.course = Course.objects.create(
            code="CS101",
            title="Introduction to Computer Science",
            description="A basic course on computer science",
            school=self.school,
        )
        self.assignment = Assignment.objects.create(
            course=self.course,
            title="Assignment 1",
            description="First assignment",
            due_date="2024-07-10 23:59:59",
            file="assignments/assignment1.pdf",
        )

    def test_assignment_creation(self):
        self.assertEqual(self.assignment.title, "Assignment 1")
        self.assertEqual(self.assignment.course, self.course)
        self.assertEqual(str(self.assignment), "Assignment 1")

    def test_get_absolute_url(self):
        self.assertEqual(self.assignment.get_absolute_url(), reverse('assignment_detail', kwargs={'pk': self.assignment.pk}))

class QuestionModelTest(TestCase):

    def setUp(self):
        self.question = Question.objects.create(
            text="What is the capital of France?",
            question_type="MCQ",
        )

    def test_question_creation(self):
        self.assertEqual(self.question.text, "What is the capital of France?")
        self.assertEqual(self.question.question_type, "MCQ")
        self.assertEqual(str(self.question), "What is the capital of France?")

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = BaseUser.objects.create_user(
            username='testuser',
            password='complex_password_123',
            email='testuser@example.com'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio="This is a test bio",
            location="Test City",
            birth_date="1990-01-01",
            avatar="avatars/test_avatar.png",
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.bio, "This is a test bio")
        self.assertEqual(str(self.profile), "testuser's profile")





# class StudentCRUDTest(TestCase):

#     def setUp(self):
#         self.user = Student.objects.create_user(
#             first_name='Test',
#             last_name='User',
#             username='testuser',
#             password='complex_password_123',
#             email='testuser@example.com',
#             school='1',
#             UID='123456',

#         )

#     def test_create_student(self):
#         response = self.client.post(reverse('student_create'), {
#             'name': 'John Doe',
#             'email': 'john@example.com'
#         })
#         self.assertEqual(response.status_code, 302)  # Redirects after successful creation
#         self.assertTrue(Student.objects.filter(name='John Doe').exists())

#     def test_read_student(self):
#         student = Student.objects.create(name='John Doe', email='john@example.com')
#         response = self.client.get(reverse('student_detail', kwargs={'pk': student.pk}))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'John Doe')

#     def test_update_student(self):
#         student = Student.objects.create(name='John Doe', email='john@example.com')
#         response = self.client.post(reverse('student_update', kwargs={'pk': student.pk}), {
#             'name': 'Jane Doe',
#             'email': 'jane@example.com'
#         })
#         self.assertEqual(response.status_code, 302)  # Redirects after successful update
#         student.refresh_from_db()
#         self.assertEqual(student.name, 'Jane Doe')
#         self.assertEqual(student.email, 'jane@example.com')

#     def test_delete_student(self):
#         student = Student.objects.create(name='John Doe', email='john@example.com')
#         response = self.client.post(reverse('student_delete', kwargs={'pk': student.pk}))
#         self.assertEqual(response.status_code, 302)  # Redirects after successful deletion
#         self.assertFalse(Student.objects.filter(name='John Doe').exists())


# class DashboardViewTest(TestCase):
#     def test_dashboard_view(self):
#         client = Client()
#         response = client.get('/dashboard/')
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Dashboard')
#         self.assertTemplateUsed(response, 'dashboard.html')
#         self.assertTemplateUsed(response, 'base.html')
#         self.assertTemplateUsed(response, 'navbar.html')