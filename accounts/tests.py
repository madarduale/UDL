from django.test import TestCase
from django.urls import reverse
# from django.contrib.auth.models import BaseUser
from udl_app.models import Student, BaseUser

# class StudentSignupTest(TestCase):
#     def setUp(self):
#         pass

#     def test_student_signup(self):
#         response = self.client.post(reverse('student/signup/'), {
#             'username': 'testuser',
#             'first_name': 'Test',
#             'last_name': 'User',
#             'password1': 'complex_password_123',
#             'password2': 'complex_password_123',
#             'email': 'testuser@example.com',
#             'school': 'test school',
#             'UID': '123456',
#         })
#         self.assertEqual(response.status_code, 302)  # Redirects after successful signup
#         self.assertTrue(BaseUser.objects.filter(username='testuser').exists())

class StudentCRUDTest(TestCase):

    def setUp(self):
        self.user = BaseUser.objects.create_user(
            username='testuser',
            password='complex_password_123',
            email='testuser@example.com'
        )

    def test_create_student(self):
        response = self.client.post(reverse('student_create'), {
            'name': 'John Doe',
            'email': 'john@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation
        self.assertTrue(Student.objects.filter(name='John Doe').exists())

    def test_read_student(self):
        student = Student.objects.create(name='John Doe', email='john@example.com')
        response = self.client.get(reverse('student_detail', kwargs={'pk': student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_update_student(self):
        student = Student.objects.create(name='John Doe', email='john@example.com')
        response = self.client.post(reverse('student_update', kwargs={'pk': student.pk}), {
            'name': 'Jane Doe',
            'email': 'jane@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful update
        student.refresh_from_db()
        self.assertEqual(student.name, 'Jane Doe')
        self.assertEqual(student.email, 'jane@example.com')

    def test_delete_student(self):
        student = Student.objects.create(name='John Doe', email='john@example.com')
        response = self.client.post(reverse('student_delete', kwargs={'pk': student.pk}))
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion
        self.assertFalse(Student.objects.filter(name='John Doe').exists())
