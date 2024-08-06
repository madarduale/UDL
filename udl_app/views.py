from django.shortcuts import render, redirect
import jwt
import json
from .jaas_jwt import JaaSJwtBuilder
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from .searchs import SearchView
from collections import defaultdict
from django.db.models import Count
import weasyprint
from weasyprint import HTML
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from .forms import (
    MessageForm, CourseForm, LectureForm,
    AssignmentForm, AssigmmentGradeForm, AssignmentSubmissionForm,
    ExamForm, ExamGradingForm, ExamSubmissionForm,
    QuestionForm, SchoolForm, SemesterForm,
    ChoiceForm, ResourceForm, EnrolledCourseForm,
    DiscussionForm, CommentForm, ProfileForm,
    ZoomMeetingForm, AdminForm, ProfessorForm, StudentForm, BaseUserForm
)

from django.shortcuts import render, get_object_or_404, redirect
from .models import(
    Admin, Professor, Student, Course, Lecture, Grade,
    Assignment, AssignmentGrade, AssignmentSubmission,
    Exam, ExamGrading, ExamSubmission, Semester,
    Question, Choice, Resource, EnrolledCourse,
    Discussion, Comment, Profile, LectureProgress,
    School, Message, ZoomMeeting, BaseUser, LectureQuestions
) 

from .decorators import(
admin_required, professor_required, student_required, 
admin_or_professor_required, admin_or_professor_or_student_required, 
admin_or_superuser_required, superuser_required, admin_or_superuser_or_professor_required,
admin_or_superuser_or_profeesor_or_student_required,
)



@login_required
def student_pdf(request, student_id):
    user = Student.objects.get(id=student_id)
    profile = Profile.objects.get(user=user)
    exam_grades = ExamGrading.objects.filter(student=user)
    assignment_grades = AssignmentGrade.objects.filter(student=user)
    enrolled_courses = EnrolledCourse.objects.filter(student=user)
    courses = []
    for enrolled_course in enrolled_courses:
        courses.extend(Course.objects.filter(enrolled_course=enrolled_course))
  
    template_name = 'students/student_pdf.html'
    avatar_url = None
    if profile.avatar:
        avatar_url = request.build_absolute_uri(profile.avatar.url)
    html_string = render_to_string(template_name, {
        'user': user,
        'profile': profile,
        'exam_grades': exam_grades,
        'assignment_grades': assignment_grades ,
        'avatar_url': avatar_url,
        'courses': courses
    })

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_info.pdf"'
    weasyprint.HTML(string=html_string).write_pdf(response)

    return response

@login_required
def students_pdf(request):
    user = request.user
    students = []
    if user.is_superuser:
        students = Student.objects.all()
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            students.extend(Student.objects.filter(school=school))
    
    # Generate the HTML content for all students
    html_string = ""
    for student in students:
        profile = Profile.objects.get(user=student)
        exam_grades = ExamGrading.objects.filter(student=student)
        assignment_grades = AssignmentGrade.objects.filter(student=student)
        enrolled_courses = EnrolledCourse.objects.filter(student=student)
        courses = []
        for enrolled_course in enrolled_courses:
            courses.extend(Course.objects.filter(enrolled_course=enrolled_course))
        template_name = 'students/student_pdf.html'
        avatar_url = None
        if profile.avatar:
            avatar_url = request.build_absolute_uri(profile.avatar.url)
        html_string += render_to_string(template_name, {
            'user': student,
            'profile': profile,
            'exam_grades': exam_grades,
            'assignment_grades': assignment_grades,
            'avatar_url': avatar_url,
            'courses': courses
        })

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students_info.pdf"'
    weasyprint.HTML(string=html_string).write_pdf(response)


    return response



@login_required
def professor_pdf(request, professor_id):
    user = Professor.objects.get(id=professor_id)
    profile = Profile.objects.get(user=user)
    courses = Course.objects.filter(professors=user)
    template_name = 'professors/professor_pdf.html'
    avatar_url = None
    if profile.avatar:
        avatar_url = request.build_absolute_uri(profile.avatar.url)
     # Render HTML template with context data
    html_string = render_to_string(template_name, {
        'user': user,
        'profile': profile,
        # 'exam_grades': exam_grades if user_type == 'student' else None,
        # 'assignment_grades': assignment_grades if user_type == 'student' else None,
        'courses': courses,
        'avatar_url': avatar_url 
    })

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_info.pdf"'
    weasyprint.HTML(string=html_string).write_pdf(response)

    return response

@login_required
def professors_pdf(request):
    user = request.user
    professors = []
    
    if user.is_superuser:
        professors = Professor.objects.all()
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            professors.extend(Professor.objects.filter(school=school))
    
    
    # Generate the HTML content for all professors
    html_string = ""
    for professor in professors:
        profile = Profile.objects.get(user=professor)
        courses = Course.objects.filter(professors=professor)
        template_name = 'professors/professor_pdf.html'

                # Construct the absolute URL for the avatar
        avatar_url = None
        if profile.avatar:
            avatar_url = request.build_absolute_uri(profile.avatar.url)

        html_string += render_to_string(template_name, {
            'user': professor,
            'profile': profile,
            'courses': courses ,
            'avatar_url': avatar_url
        })
    #page break
    # html_string += '<div class="page-break"></div>'

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="professors_info.pdf"'
    HTML(string=html_string).write_pdf(response)
    
    return response




@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'udl_app/home.html')


def video_call(request):
    return render(request, 'udl_app/video.html')

@login_required
def professor_video_call(request, exam_id):
    user = request.user
    if not user.is_professor:
        return HttpResponseForbidden("You are not authorized to access this page.")

    exam = get_object_or_404(Exam, pk=exam_id)
    return render(request, 'professors/professor_video_call.html', {'exam': exam, 'professor_id': user.id})


def generate_jwt(user):
    jaas_jwt = JaaSJwtBuilder()
    private_key = settings.JWT_PRIVATE_KEY.strip() 

    token = jaas_jwt.withDefaults() \
        .withApiKey("vpaas-magic-cookie-943c0882125d4e38beba77d5b36093a7/45e73f") \
        .withUserName(user.username) \
        .withUserEmail(user.email) \
        .withModerator(user.is_admin or user.is_professor) \
        .withAppID("vpaas-magic-cookie-943c0882125d4e38beba77d5b36093a7") \
        .withUserAvatar(user.profile.avatar.url if user.profile.avatar else '') \
        .signWith(private_key)

    return token



def jitsi_meet(request):
    # jwt_token = generate_jwt(request.user)
    jwt_token = generate_jwt(request.user)
    # decoded_token = jwt.decode(jwt_token, verify=False, algorithms=['RS256']) 
    decoded_token = jwt_token.decode("utf-8")

    # jwt_token2='eyJraWQiOiJ2cGFhcy1tYWdpYy1jb29raWUtOTQzYzA4ODIxMjVkNGUzOGJlYmE3N2Q1YjM2MDkzYTcvZWIwOWViLVNBTVBMRV9BUFAiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJqaXRzaSIsImlzcyI6ImNoYXQiLCJpYXQiOjE3MTQ4NTQyNTEsImV4cCI6MTcxNDg2MTQ1MSwibmJmIjoxNzE0ODU0MjQ2LCJzdWIiOiJ2cGFhcy1tYWdpYy1jb29raWUtOTQzYzA4ODIxMjVkNGUzOGJlYmE3N2Q1YjM2MDkzYTciLCJjb250ZXh0Ijp7ImZlYXR1cmVzIjp7ImxpdmVzdHJlYW1pbmciOnRydWUsIm91dGJvdW5kLWNhbGwiOnRydWUsInNpcC1vdXRib3VuZC1jYWxsIjpmYWxzZSwidHJhbnNjcmlwdGlvbiI6dHJ1ZSwicmVjb3JkaW5nIjp0cnVlfSwidXNlciI6eyJoaWRkZW4tZnJvbS1yZWNvcmRlciI6ZmFsc2UsIm1vZGVyYXRvciI6dHJ1ZSwibmFtZSI6Im1hZGFyZHVjYWFsZTk5ODgiLCJpZCI6ImF1dGgwfDY2MzVkNTc4NjFhOTRkZGMzNjA2NzU5NCIsImF2YXRhciI6IiIsImVtYWlsIjoibWFkYXJkdWNhYWxlOTk4OEBnbWFpbC5jb20ifX0sInJvb20iOiIqIn0.TzxGx5krRc0AM7xKo0F5iHb6vZoGngmjj8uO-F-wHE_VTg9qVL_HS0nPuANP35jaiyZqJakWv3P2KZwCyCc49tCTk8XOc7MuHj7vWetKTdao-Kj_IC9gZipX2peBCeGWOdZe2gWQ-Skj2GT6-h90sl_D6916rdYonoKZBTwzjOOympJNh3YKAQ4DIbmiV4K34vgg2bY6wFRCBnVL5g5fQAbcVwIOIVco7gvJjCgukXwkho-wCRHl8VWJgDQKVVhBA-pGvsHU7v41kKLGRxyz6QK9FOfWML0mQikL7G9tOkj3tm0KXlUQESfUnDQbCpToZbsF9kzbMZBRPlELWP4-Ug'
    return render(request, 'udl_app/jitsi_meet.html', {'jwt_token': decoded_token})


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request=request)
        if form.is_valid():
            message = form.save(commit=False)
            recipients = None
            students = form.cleaned_data['students']
            professors = form.cleaned_data['professors']
            admins = form.cleaned_data['admins']

            if request.user.is_superuser:
                recipients = form.cleaned_data['students'] | form.cleaned_data['professors'] | form.cleaned_data['admins']
            elif request.user.is_admin:
                recipients = form.cleaned_data['students'] | form.cleaned_data['professors']
            elif request.user.is_professor:
                recipients = list(students)+list(admins)
            elif request.user.is_student:
                recipients = form.cleaned_data['professors'] | form.cleaned_data['admins']
            
            message.sender = request.user
            message.save()
            if recipients:
                message.recipients.set(recipients)
            messages.success(request, 'Message sent successfully!')
            return redirect('message_list') 
    else:
        form = MessageForm(request=request)
    return render(request, 'udl_app/send_message.html', {'form': form})

def get_unread_message_count(user):
    return Message.objects.filter(recipients=user, is_read=False).count()



@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipients=request.user).order_by('-timestamp')
    unread_count = get_unread_message_count(request.user)
    jwt_token = generate_jwt(request.user)
    decoded_token = jwt_token.decode("utf-8")
    message_urls = []  
    for message in received_messages:
        if not message.is_read:
            message.is_read = True
            message.save()
        if message.url:
            meeting_url = f'{message.url}?jwt={decoded_token}'
            message_urls.append((message, meeting_url))
        else:
            message_urls.append((message, None))
    return render(request, 'udl_app/inbox.html', {'message_urls':message_urls})


@login_required
def unread_count(request):
    unread_count = get_unread_message_count(request.user)
    return JsonResponse({'unread_count': unread_count})


@login_required
def dashboard(request):
    user = request.user

    # Initialize all counts to 0
    count_students = 0
    count_admins = 0
    count_professors = 0
    count_courses = 0
    count_lectures = 0
    count_schools = 0
    count_exams = 0

    if user.is_superuser:
        count_students = Student.objects.count()
        count_admins = Admin.objects.count()
        count_professors = Professor.objects.count()
        count_courses = Course.objects.count()
        count_lectures = Lecture.objects.count()
        count_schools = School.objects.count()
        count_exams = Exam.objects.count()
    elif user.is_admin:
        admin = Admin.objects.get(id=user.id)
        schools = admin.school.all()
        count_schools = schools.count()

        for school in schools:
            count_students += Student.objects.filter(school=school).count()
            count_professors += Professor.objects.filter(school=school).count()
            count_courses += Course.objects.filter(school=school).count()
            count_lectures += Lecture.objects.filter(course__school=school).count()
            count_exams += Exam.objects.filter(course__school=school).count()
        
        count_admins = 1  # The current admin user
    elif user.is_professor:
        professor = Professor.objects.get(id=user.id)
        count_professors = 1  # The current professor user
        count_courses = professor.courses_taught.count()
        count_lectures = Lecture.objects.filter(course__professors=professor).count()
        count_exams = Exam.objects.filter(course__professors=professor).count()
        count_students = Student.objects.filter(enrolled_student__course__professors=professor).count()
        count_schools = professor.school.count()
        count_admins = Admin.objects.filter(school__proffesor_school=professor).count()
    elif user.is_student:
        student = Student.objects.get(id=user.id)
        count_students = 1  # The current student user
        count_courses = student.enrolled_student.count()
        enrolled_courses = student.enrolled_student.all()
        count_lectures = Lecture.objects.filter(course__in=[ec.course for ec in enrolled_courses]).count()
        count_exams = ExamSubmission.objects.filter(student=student).count()
        count_schools = student.school.count()
        count_admins = Admin.objects.filter(school__student_school=student).count()
        count_professors = Professor.objects.filter(school__student_school=student).count()

    return render(request, 'dashboard.html', {
        'count_students': count_students,
        'count_admins': count_admins,
        'count_professors': count_professors,
        'count_courses': count_courses,
        'count_lectures': count_lectures,
        'count_schools': count_schools,
        'count_exams': count_exams
    })


@login_required
def course_list(request):
    user = request.user
    if user.is_superuser:
        courses = Course.objects.all()
        return render(request, 'courses/course_list.html', {'courses': courses})
    elif user.is_admin:
        form = CourseForm(user=request.user)
        if request.method == 'POST':
            course_create(request)
        course=None
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            courses = Course.objects.filter(school=school)
        return render(request, 'courses/course_list.html', {'courses': courses, 'form': form})
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        courses = professor.courses_taught.all()
        return render(request, 'courses/course_list.html', {'courses': courses})
    elif user.is_student:
        student = get_object_or_404(Student, id=user.id)
        courses=None
        for school in student.school.all():
            courses = Course.objects.filter(school=school)
        return render(request, 'courses/course_list.html', {'courses': courses})
    else:
        return render(request, 'courses/course_list.html', {'courses': 'No course'})
    
# not working
@login_required
def school_course(request):
    user = request.user
    if user.is_student:
        student = get_object_or_404(Student, id=user.id)
        school_courses = Course.objects.filter(school=student.school) 
        return render(request, 'courses/school_course.html', {'school_courses': school_courses})
    return render(request, 'courses/school_course.html', {'school_courses': 'No courses'})
     

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(instance=course, user=request.user)
    if request.method == 'POST':
        course_edit(request, pk)
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course, 'form': form})

@login_required
@admin_or_superuser_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(user=request.user)
    return render(request, 'courses/course_create.html', {'form': form})

@login_required
@admin_or_superuser_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST,  request.FILES, instance=course, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_detail', pk=pk)
    else:
        form = CourseForm(instance=course, user=request.user)
    return render(request, 'courses/course_edit.html', {'form': form, 'course': course})

@login_required
@admin_or_superuser_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@login_required
# @superuser_required
def school_list(request):
    form = SchoolForm()

    user = request.user
    if user.is_superuser:
        schools = School.objects.annotate(course_count=Count('courses_school'))
        if request.method == 'POST':
            school_create(request)
        return render(request, 'schools/school_list.html', {'schools': schools, 'form':form})
    elif user.is_admin:
        # admin = get_object_or_404(Admin, id=user.id)
        schools = School.objects.filter(admin_school=user).annotate(course_count=Count('courses_school'))
        return render(request, 'schools/school_list.html', {'schools': schools})
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        schools = professor.school.all().annotate(course_count=Count('courses_school'))
        return render(request, 'schools/school_list.html', {'schools': schools})
    elif user.is_student:
        # student = get_object_or_404(Student, id=user.id)
        # schools = student.school.all().annotate(course_count=Count('courses_school'))
        schools = School.objects.filter(student_school=user).annotate(course_count=Count('courses_school'))
        return render(request, 'schools/school_list.html', {'schools': schools})
    else:
        return render(request, 'schools/school_list.html', {'schools': 'No school'})

@login_required
@superuser_required
def school_detail(request, pk):
    school = get_object_or_404(School, pk=pk)
    form = SchoolForm(instance=school)
    if request.method == 'POST':
        school_edit(request, pk)
    return render(request, 'schools/school_detail.html', {'school': school, 'form':form})


@login_required
@superuser_required
def school_create(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'School created successfully!')
            return redirect('school_list')
    else:
        form = SchoolForm()
    return render(request, 'schools/school_create.html', {'form': form})

@login_required
@superuser_required
def school_edit(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, 'School updated successfully!')
            return redirect('school_list')
    else:
        form = SchoolForm(instance=school)
    return render(request, 'schools/school_edite.html', {'form': form})

@login_required
@superuser_required
def school_delete(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        school.delete()
        messages.success(request, 'School deleted successfully!')
        return redirect('school_list')
    return render(request, 'schools/school_confirm_delete.html', {'school': school})

@login_required
@admin_or_superuser_required
def semester_list(request):
    form = SemesterForm()
    semesters = Semester.objects.all()
    if request.method == 'POST':
        semester_create(request)
    return render(request, 'semesters/semester_list.html', {'semesters': semesters, 'form': form})

@login_required
@admin_or_superuser_required
def semester_detail(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    form = SemesterForm(instance=semester)
    if request.method == 'POST':
        semester_edit(request, pk)  
    return render(request, 'semesters/semester_detail.html', {'semester': semester, 'form': form})

@login_required
@admin_or_superuser_required
def semester_create(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Semester created successfully!')
            return redirect('semester_list')
    else:
        form = SemesterForm()
    return render(request, 'semesters/semester_create.html', {'form': form})

@login_required
@admin_or_superuser_required
def semester_edit(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            messages.success(request, 'Semester updated successfully!')
            return redirect('semester_list')
    else:
        form = SemesterForm(instance=semester)
    return render(request, 'semesters/semester_edite.html', {'form': form})

@login_required
@admin_or_superuser_required
def semester_delete(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        semester.delete()
        messages.success(request, 'Semester deleted successfully!')
        return redirect('semester_list')
    return render(request, 'semesters/semester_confirm_delete.html', {'semester': semester})

@login_required
def complete_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    student = get_object_or_404(Student, id=request.user.id)

    if request.method == 'POST':
        # Mark the lecture as completed
        LectureProgress.objects.update_or_create(
            student=student,
            lecture=lecture,
            defaults={'completed': True},
        )

        # Redirect to the next lecture or lecture list
        next_lecture = Lecture.objects.filter(course=lecture.course, id__gt=lecture.id).first()
        if next_lecture:
            return redirect('lecture_detail', next_lecture.pk)
        else:
            messages.success(request, 'Course completed successfully!, Congratulations!👏🎉🎈')
            return redirect('enrolled_course_list')
    return render(request, 'lectures/lecture_detail.html', {'lecture': lecture})

@login_required
def incomplete_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    student = get_object_or_404(Student, id=request.user.id)

    if request.method == 'POST':
        # Mark the lecture as incomplete
        LectureProgress.objects.filter(student=student, lecture=lecture).delete()

        # Redirect to the lecture detail
        return redirect('lecture_detail', pk=lecture_id)
    return render(request, 'lectures/lecture_detail.html', {'lecture': lecture})

@login_required
# @admin_or_professor_required
def lecture_list(request):
    user = request.user
    form = LectureForm(user=request.user)
    if request.method == 'POST':
        lecture_create(request)
    
    if user.is_superuser:
        lectures = Lecture.objects.all().order_by('id')
        grouped_by_course = defaultdict(list)
        for lecture in lectures:
            grouped_by_course[lecture.course].append(lecture)
        return render(request, 'lectures/lecture_list.html', {'lectures': lectures, 'grouped_by_course': dict(grouped_by_course),  'form': form}) 
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            lectures = Lecture.objects.filter(course__school=school).order_by('id')
        grouped_by_course = defaultdict(list)
        for lecture in lectures:
            grouped_by_course[lecture.course].append(lecture)
        return render(request, 'lectures/lecture_list.html', {'lectures': lectures, 'grouped_by_course': dict(grouped_by_course), 'form': form}) 
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        lectures = Lecture.objects.filter(course__professors=professor).order_by('id')
        grouped_by_course = defaultdict(list)
        for lecture in lectures:
            grouped_by_course[lecture.course].append(lecture)
        return render(request, 'lectures/lecture_list.html', {'lectures': lectures, 'grouped_by_course': dict(grouped_by_course), 'form': form})
    elif user.is_student:
        student = get_object_or_404(Student, id=user.id)
        enrolled_course = EnrolledCourse.objects.filter(student=student)
        lectures = Lecture.objects.filter(course__in=enrolled_course.values('course')).order_by('id')
        # lectures = Lecture.objects.filter(course__students=student)
        progress = LectureProgress.objects.filter(student=student)
        progress_dict = {p.lecture.id: p.completed for p in progress}
        grouped_by_course = defaultdict(list)
        for lecture in lectures:
            lecture.is_completed = progress_dict.get(lecture.id, False)
            grouped_by_course[lecture.course].append(lecture)
        return render(request, 'lectures/lecture_list.html', {'lectures': lectures, 'grouped_by_course': dict(grouped_by_course), 'form': form})
    else:
        lectures = Lecture.objects.none()
        return render(request, 'lectures/lecture_list.html', {'lectures': lectures,  'form': form}) 

@login_required
def student_course_lectures(request, pk):
    student = get_object_or_404(Student, id=request.user.id)
    course = get_object_or_404(Course, pk=pk)
    lectures = Lecture.objects.filter(course=course).order_by('id')
    progress = LectureProgress.objects.filter(student=student)
    progress_dict = {p.lecture.id: p.completed for p in progress}
    grouped_by_course = defaultdict(list)
    for lecture in lectures:
        lecture.is_completed = progress_dict.get(lecture.id, False)
        grouped_by_course[lecture.course].append(lecture)
    return render(request, 'lectures/student_course_lectures.html', {'lectures': lectures, 'course': course, 'grouped_by_course': dict(grouped_by_course)})



@login_required
def lecture_detail(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    resource = Resource.objects.filter(lecture=lecture).order_by('id')
    form = LectureForm(instance=lecture, user=request.user)
    if request.method == 'POST':
        lecture_edit(request, pk)
    if request.user.is_student:
        student = get_object_or_404(Student, id=request.user.id)
        completed = LectureProgress.objects.filter(student=student, lecture=lecture).exists()
        previous_lecture = Lecture.objects.filter(course=lecture.course, id__lt=lecture.id).order_by('-id').first()
        if previous_lecture:
            previous_progress = LectureProgress.objects.filter(student=student, lecture=previous_lecture, completed=True).exists()
            if not previous_progress:
                messages.error(request, 'You must complete the previous lecture first!')
                return redirect('student__course_lectures', lecture.course.pk)
            return render(request, 'lectures/lecture_detail.html', {'lecture': lecture, 'form': form,  'resource': resource, 'completed':completed})
    return render(request, 'lectures/lecture_detail.html', {'lecture': lecture, 'form': form})

@login_required
@admin_or_professor_required
def lecture_create(request):
    if request.method == 'POST':
        form = LectureForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lecture created successfully!')
            return redirect('lecture_list')
    else:
        form = LectureForm(user=request.user)
    return render(request, 'lectures/lecture_create.html', {'form': form})

@login_required
@admin_or_professor_required
def lecture_edit(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    if request.method == 'POST':
        form = LectureForm(request.POST, instance=lecture)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lecture updated successfully!')
            return redirect('lecture_list')
    else:
        form = LectureForm(instance=lecture)
    return render(request, 'lectures/lecture_edite.html', {'form': form, 'lecture': lecture})

@login_required
@admin_or_professor_required
def lecture_delete(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    if request.method == 'POST':
        lecture.delete()
        messages.success(request, 'Lecture deleted successfully!')
        return redirect('lecture_list')
    return render(request, 'lectures/lecture_confirm_delete.html', {'lecture': lecture})



@login_required
def assignment_list(request):
    user = request.user
    form = AssignmentForm(user=request.user)
    current_time = timezone.now()
    form2 = AssignmentSubmissionForm(user=request.user)
    if request.method == 'POST':
        assignment_create(request)
        assignment_submission_create(request)
    if user.is_superuser:
        assignments = Assignment.objects.all()
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            assignments = Assignment.objects.filter(course__school=school)
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        assignments = Assignment.objects.filter(course__professors=professor)
    elif user.is_student:
        student = get_object_or_404(Student, id=user.id)
        enrolled_course = EnrolledCourse.objects.filter(student=student)
        assignments = Assignment.objects.filter(course__in=enrolled_course.values('course'))
    else:
        assignments = Assignment.objects.none()
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments, 'form': form, 'form2': form2, 'current_time': current_time})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    form = AssignmentForm(instance=assignment, user=request.user)
    if request.method == 'POST':
        assignment_edit(request, pk)
    return render(request, 'assignments/assignment_detail.html', {'assignment': assignment, 'form': form})

@login_required
def assignment_create(request):
    user = request.user
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(user=user)
    return render(request, 'assignments/assignment_create.html', {'form': form})

@login_required
def assignment_edit(request, pk):
    user = request.user
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment, user=user)
    return render(request, 'assignments/assignment_edite.html', {'form': form, 'assignment': assignment})

@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully!')
        return redirect('assignment_list')
    return render(request, 'assignments/assignment_confirm_delete.html', {'assignment': assignment})



@login_required
def assignment_submission_list(request):
    form = AssigmmentGradeForm(user=request.user)
    if request.method == 'POST':
        assignment_grade_create(request)
    if request.user.is_superuser:
        assignment_submissions = AssignmentSubmission.objects.all()
    elif request.user.is_admin:
        admin = get_object_or_404(Admin, id=request.user.id)
        for school in admin.school.all():
            assignment_submissions = AssignmentSubmission.objects.filter(assignment__course__school=school)
    elif request.user.is_professor:
        professor = get_object_or_404(Professor, id=request.user.id)
        assignment_submissions = AssignmentSubmission.objects.filter(assignment__course__professors=professor)
    elif request.user.is_student:
        student = get_object_or_404(Student, id=request.user.id)
        assignment_submissions = AssignmentSubmission.objects.filter(student=student)
    else:
        assignment_submissions = AssignmentSubmission.objects.none()
    return render(request, 'assignment_submissions/assignment_submission_list.html', {'assignment_submissions': assignment_submissions, 'form': form})


@login_required
def assignment_submission_detail(request, pk):
    assignment_submission = get_object_or_404(AssignmentSubmission, pk=pk)
    form  = AssignmentSubmissionForm(user=request.user, instance=assignment_submission)
    if request.method == 'POST':
        assignment_submission_edit(request, pk)
    return render(request, 'assignment_submissions/assignment_submission_detail.html', {'assignment_submission': assignment_submission, 'form': form})


@login_required
def assignment_submission_create(request):
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages
            return redirect('assignment_submission_list')
    else:
        form = AssignmentSubmissionForm(user=request.user)
    return render(request, 'assignment_submissions/assignment_submission_create.html', {'form': form})


@login_required
def assignment_submission_edit(request, pk):
    assignment_submission = get_object_or_404(AssignmentSubmission, pk=pk)
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST,  request.FILES, instance=assignment_submission, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment submission updated successfully!')
            return redirect('assignment_submission_list')
    else:
        form = AssignmentSubmissionForm(instance=assignment_submission, user=request.user)
    return render(request, 'assignment_submissions/assignment_submission_form.html', {'form': form})


@login_required
def assignment_submission_delete(request, pk):
    assignment_submission = get_object_or_404(AssignmentSubmission, pk=pk)
    if request.method == 'POST':
        assignment_submission.delete()
        messages.success(request, 'Assignment submission deleted successfully!')
        return redirect('assignment_submission_list')
    return render(request, 'assignment_submissions/assignment_submission_confirm_delete.html', {'assignment_submission': assignment_submission})


@login_required
def assignment_grade_list(request):
    if request.user.is_superuser:
        assignment_grades = AssignmentGrade.objects.all()
    elif request.user.is_admin:
        admin = get_object_or_404(Admin, id=request.user.id)
        for school in admin.school.all():
            assignment_grades = AssignmentGrade.objects.filter(assignment_solution__assignment__course__school=school)
    elif request.user.is_professor:
        professor = get_object_or_404(Professor, id=request.user.id)
        assignment_grades = AssignmentGrade.objects.filter(assignment_solution__assignment__course__professors=professor)
    elif request.user.is_student:
        student = get_object_or_404(Student, id=request.user.id)
        assignment_grades = AssignmentGrade.objects.filter(assignment_solution__student=student)
    else:
        assignment_grades = AssignmentGrade.objects.none()
    return render(request, 'assignment_grades/assignment_grade_list.html', {'assignment_grades': assignment_grades})    


@login_required 
def assignment_grade_detail(request, pk):
    assignment_grade = get_object_or_404(AssignmentGrade, pk=pk)
    form = AssigmmentGradeForm(instance=assignment_grade, user=request.user)
    if request.method == 'POST':
        assignment_grade_edit(request, pk)
    return render(request, 'assignment_grades/assignment_grade_detail.html', {'assignment_grade': assignment_grade, 'form': form})


@login_required
def assignment_grade_create(request):
    if request.method == 'POST':
        form = AssigmmentGradeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment graded successfully!')
            return redirect('assignment_grade_list')
    else:
        form = AssigmmentGradeForm(user=request.user)

    return render(request, 'assignment_grades/assignment_grade_create.html', {'form': form})


@login_required
def assignment_grade_edit(request, pk):
    assignment_grade = get_object_or_404(AssignmentGrade, pk=pk)
    if request.method == 'POST':
        form = AssigmmentGradeForm(request.POST, instance=assignment_grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment grade updated successfully!')
            return redirect('assignment_grade_list')
    else:
        form = AssigmmentGradeForm(instance=assignment_grade)
    return render(request, 'assignment_grades/assignment_grade_edite.html', {'form': form})


@login_required
def assignment_grade_delete(request, pk):
    assignment_grade = get_object_or_404(AssignmentGrade, pk=pk)
    if request.method == 'POST':
        assignment_grade.delete()
        messages.success(request, 'Assignment grade deleted successfully!')
        return redirect('assignment_grade_list')
    return render(request, 'assignment_grades/assignment_grade_confirm_delete.html', {'assignment_grade': assignment_grade})



@login_required
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam created successfully!')
            return redirect('exam_list')
    else:
        form = ExamForm(user=request.user)
    return render(request, 'exams/exam_create.html', {'form': form})


@login_required
def exam_list(request):
    form = ExamForm(user=request.user)
    form2 = ExamSubmissionForm(user=request.user)
    form3 = QuestionForm(user=request.user)
    form4 = ChoiceForm(user=request.user)
    current_time = timezone.now()
    exams = None
    if request.method == 'POST':
        exam_create(request)
        # exam_submission_create(request)
        question_create(request)
        choice_create(request)
    if request.user.is_superuser:
        exams = Exam.objects.all()
    elif request.user.is_admin:
        admin = get_object_or_404(Admin, id=request.user.id)
        for school in admin.school.all():
            exams = Exam.objects.filter(course__school=school)
    elif request.user.is_professor:
        professor = get_object_or_404(Professor, id=request.user.id)
        exams = Exam.objects.filter(course__professors=professor)
    elif request.user.is_student:
        student = get_object_or_404(Student, id=request.user.id)
        enrolled_course = EnrolledCourse.objects.filter(student=student)
        exams = Exam.objects.filter(course__in=enrolled_course.values('course'))
    else:
        exams = Exam.objects.none()
    return render(request, 'exams/exam_list.html', {'exams': exams, 'form': form, 'form2': form2, 'current_time': current_time, 'form3': form3, 'form4': form4})


@login_required
def exam_detail(request, pk):
    user = request.user
    studentid=None
    if user.is_student:
        studentid = get_object_or_404(Student, id=user.id) 
    exam = get_object_or_404(Exam, pk=pk)
    submited_exams = ExamSubmission.objects.filter(exam=exam)

    for submited_exam in submited_exams:
        if submited_exam.student.id == user.id:
            messages.error(request, 'You have already submited the exam!')
            return redirect('exam_list')
        
    group_questions_by_type = defaultdict(list)
    for question in exam.questions.all():
        group_questions_by_type[question.question_type].append(question)
    form = ExamForm(instance=exam, user=request.user)
    current_time = timezone.now()
    if request.method == 'POST':
        exam_edit(request, pk)
    professor_id = exam.course.professors.first().id
    return render(request, 'exams/exam_detail.html', {
        'exam': exam,
        'form': form, 
        'current_time': current_time, 
        'group_questions_by_type': dict(group_questions_by_type),
        'professor_id': professor_id,
        'studentid': studentid
        })


@login_required
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated successfully!')
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'exams/exam_edite.html', {'form': form, 'exam': exam})


@login_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully!')
        return redirect('exam_list')
    return render(request, 'exams/exam_confirm_delete.html', {'exam': exam})


@login_required
def exam_submission_list_by_id(request, exam_id):
    form = ExamGradingForm(user=request.user)
    if request.method == 'POST':
        exam_grading_create(request)

    exam = get_object_or_404(Exam, pk=exam_id)
    submissions = ExamSubmission.objects.filter(exam=exam)
    submission_data = []
    for submission in submissions:
        student_answers = []
        for question_id, answer in submission.answers.items():
            question = get_object_or_404(Question, pk=question_id)
            correct_choice = Choice.objects.filter(question=question, correct_choice=True).first()
            if isinstance(answer, int):  # MCQ or TF
                selected_choice = get_object_or_404(Choice, pk=answer)
                is_correct = selected_choice.id == correct_choice.id if correct_choice else False
                student_answers.append({
                    'question': question.question,
                    'marks': question.marks,
                    'answer': selected_choice.choice,
                    'correct_answer': correct_choice.choice if correct_choice else 'N/A',
                    'is_correct': is_correct,
                    'marks_awarded': question.marks if is_correct else 0
                })
            else:  # SA or LA
                student_answers.append({
                    'question': question.question,
                    'marks': question.marks,
                    'answer': answer,
                    'correct_answer': 'N/A',  # SA and LA need manual grading
                    'is_correct': 'N/A',
                    'marks_awarded': 'N/A'
                })
        submission_data.append({
            'student': submission.student.username,
            'submitted_at': submission.submitted_at,
            'answers': student_answers
        })

    return render(request, 'exam_submissions/exam_submission_list_by_id.html', {
        'exam': exam,
        'submission_data': submission_data,
        'form': form
    })

@login_required
def exam_submission_list(request):
    user = request.user
    if user.is_superuser:
        exam_submissions = ExamSubmission.objects.all()
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            exam_submissions = ExamSubmission.objects.filter(exam__course__school=school)
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        exam_submissions = ExamSubmission.objects.filter(exam__course__professors=professor)
    elif user.is_student:
        student = get_object_or_404(Student, id=user.id)
        exam_submissions = ExamSubmission.objects.filter(student=student)
    else:
        exam_submissions = ExamSubmission.objects.none()
    return render(request, 'exam_submissions/exam_submission_list.html', {'exam_submissions': exam_submissions})


@login_required
def exam_submission_detail(request, pk):
    exam_submission = get_object_or_404(ExamSubmission, pk=pk)
    return render(request, 'exam_submissions/exam_submission_detail.html', {'exam_submission': exam_submission})


@login_required
def exam_submission_create_by_id(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    student = get_object_or_404(Student, id=request.user.id)
    if request.method == 'POST':
        answers = {}
        for question in exam.questions.all():
            question_key = f'question{question.id}'
            if question.question_type in ['MCQ', 'TF']:
                selected_choice_id = request.POST.get(question_key)
                if selected_choice_id:
                    answers[question.id] = int(selected_choice_id)
            elif question.question_type in ['SA', 'LA']:
                written_answer = request.POST.get(question_key)
                if written_answer:
                    answers[question.id] = written_answer

        ExamSubmission.objects.create(
            exam=exam,
            student=student,
            answers=answers
        )
        # return redirect('exam_submission_list', exam_id=exam.pk)
        return redirect('exam_list')
    return render(request, 'exam_submissions/exam_submission_create_by_id.html', {'exam': exam})    

@login_required
def exam_submission_create(request):
    if request.method == 'POST':
        form = ExamSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_submission_list')
    else:
        form = ExamSubmissionForm()
    return render(request, 'exam_submissions/exam_submission_form.html', {'form': form})    


@login_required
def exam_submission_edit(request, pk):
    exam_submission = get_object_or_404(ExamSubmission, pk=pk)
    if request.method == 'POST':
        form = ExamSubmissionForm(request.POST, instance=exam_submission)
        if form.is_valid():
            form.save()
            return redirect('exam_submission_list')
    else:
        form = ExamSubmissionForm(instance=exam_submission)
    return render(request, 'exam_submissions/exam_submission_form.html', {'form': form})


@login_required
def exam_submission_delete(request, pk):
    exam_submission = get_object_or_404(ExamSubmission, pk=pk)
    if request.method == 'POST':
        exam_submission.delete()
        return redirect('exam_submission_list')
    return render(request, 'exam_submissions/exam_submission_confirm_delete.html', {'exam_submission': exam_submission})


@login_required
def exam_grading_list(request):
    user = request.user
    if user.is_superuser:
        exam_gradings = ExamGrading.objects.all()
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            exam_gradings = ExamGrading.objects.filter(submission__exam__course__school=school)
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        exam_gradings = ExamGrading.objects.filter(submission__exam__course__professors=professor)
    elif user.is_student:
        student = get_object_or_404(Student, id=user.id)
        exam_gradings = ExamGrading.objects.filter(submission__student=student)
    else:
        exam_gradings = ExamGrading.objects.none()
    return render(request, 'exam_gradings/exam_grading_list.html', {'exam_gradings': exam_gradings})


@login_required
def exam_grading_detail(request, pk):
    exam_grading = get_object_or_404(ExamGrading, pk=pk)
    form = ExamGradingForm(instance=exam_grading, user=request.user)
    if request.method == 'POST':
        exam_grading_edit(request, pk)
    return render(request, 'exam_gradings/exam_grading_detail.html', {'exam_grading': exam_grading, 'form': form})


@login_required
def exam_grading_create(request):
    if request.method == 'POST':
        form = ExamGradingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam graded successfully!')
            return redirect('exam_grading_list')
    else:
        form = ExamGradingForm(user=request.user)
    return render(request, 'exam_gradings/exam_grading_form.html', {'form': form})


@login_required
def exam_grading_edit(request, pk):
    exam_grading = get_object_or_404(ExamGrading, pk=pk)
    if request.method == 'POST':
        form = ExamGradingForm(request.POST, instance=exam_grading)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam grading updated successfully!')
            return redirect('exam_grading_list')
    else:
        form = ExamGradingForm(instance=exam_grading)
    return render(request, 'exam_gradings/exam_grading_form.html', {'form': form, 'exam_grading': exam_grading})


@login_required
def exam_grading_delete(request, pk):
    exam_grading = get_object_or_404(ExamGrading, pk=pk)
    if request.method == 'POST':
        exam_grading.delete()
        messages.success(request, 'Exam grading deleted successfully!')
        return redirect('exam_grading_list')
    return render(request, 'exam_gradings/exam_grading_confirm_delete.html', {'exam_grading': exam_grading})


@login_required
def question_list(request):
    user = request.user
    form = QuestionForm(user=request.user)
    if request.method == 'POST':
        question_create(request)

    questions = None
    questions_grouped_by_course = defaultdict(list)
    if user.is_superuser:
        questions = Question.objects.all()
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            questions = Question.objects.filter(course__school=school)
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        questions = Question.objects.filter(course__professors=professor)

    if questions:
        for question in questions:
            questions_grouped_by_course[question.course].append(question)

    return render(request, 'questions/question_list.html', {'questions': questions, 'form': form, 'questions_grouped_by_course': dict(questions_grouped_by_course)})

@login_required
@admin_or_superuser_or_professor_required
def get_questions(request):
    course_id = request.GET.get('course_id')
    # print(course_id)
    questions = Question.objects.filter(course_id=course_id)
    questions_list = list(questions.values('id', 'question'))
    return JsonResponse(questions_list, safe=False)

@login_required
def question_detail(request, pk):
    if request.method == 'POST':
        question_edit(request, pk)
    question = get_object_or_404(Question, pk=pk)
    form = QuestionForm(instance=question, user=request.user)
    return render(request, 'questions/question_detail.html', {'question': question, 'form': form})


@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question created successfully!')
            return redirect('question_list')
    else:
        form = QuestionForm(user=request.user)
    return render(request, 'questions/question_create.html', {'form': form})


@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question, user=request.user)
    return render(request, 'questions/question_edite.html', {'form': form})


@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('question_list')
    return render(request, 'questions/question_confirm_delete.html', {'question': question})


@login_required
def choice_list(request):
    form = ChoiceForm(user=request.user)
    if request.method == 'POST':
        choice_create(request)
    user = request.user
    choices = None
    choices_grouped_by_question = defaultdict(list)
    if user.is_superuser:
        choices = Choice.objects.all()
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            choices = Choice.objects.filter(question__course__school=school)
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        choices = Choice.objects.filter(question__course__professors=professor)
    if choices:
        for choice in choices:
            choices_grouped_by_question[choice.question].append(choice)
    return render(request, 'choices/choice_list.html', {'choices': choices, 'form': form, 'choices_grouped_by_question': dict(choices_grouped_by_question)})


@login_required
def choice_detail(request, pk):
    choice = get_object_or_404(Choice, pk=pk)
    return render(request, 'choices/choice_detail.html', {'choice': choice})


@login_required
def choice_create(request):
    if request.method == 'POST':
        form = ChoiceForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Choice created successfully!')
            return redirect('choice_list')
    else:
        form = ChoiceForm(user=request.user)
    return render(request, 'choices/choice_create.html', {'form': form})


@login_required
def choice_edit(request, pk):
    choice = get_object_or_404(Choice, pk=pk)
    if request.method == 'POST':
        form = ChoiceForm(request.POST, instance=choice, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Choice updated successfully!')
            return redirect('choice_list')
    else:
        form = ChoiceForm(instance=choice, user=request.user)
    return render(request, 'choices/choice_create.html', {'form': form})


@login_required
def choice_delete(request, pk):
    choice = get_object_or_404(Choice, pk=pk)
    if request.method == 'POST':
        choice.delete()
        messages.success(request, 'Choice deleted successfully!')
        return redirect('choice_list')
    return render(request, 'choices/choice_confirm_delete.html', {'choice': choice})


@login_required
def resource_list(request):
    if request.method == 'POST':
        resource_create(request)
    if request.user.is_superuser:
        resources = Resource.objects.all()
    elif request.user.is_admin:
        admin = get_object_or_404(Admin, id=request.user.id)
        for school in admin.school.all():
            lectures = Lecture.objects.filter(course__school=school)
            resources = Resource.objects.filter(lecture__in=lectures)
    elif request.user.is_professor:
        professor = get_object_or_404(Professor, id=request.user.id)
        lectures = Lecture.objects.filter(course__professors=professor)
        resources = Resource.objects.filter(lecture__in=lectures)
    elif request.user.is_student:
        student = get_object_or_404(Student, id=request.user.id)
        enrolled_course = EnrolledCourse.objects.filter(student=student)
        lectures = Lecture.objects.filter(course__in=enrolled_course.values('course'))
        resources = Resource.objects.filter(lecture__in=lectures)
    else:
        resources = Resource.objects.none()
    form = ResourceForm( user=request.user)
    return render(request, 'resources/resource_list.html', {'resources': resources, 'form': form})


@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
            resource_edit(request, pk=pk)
    form = ResourceForm(instance=resource, user=request.user)
    return render(request, 'resources/resource_detail.html', {'resource': resource, 'form': form})


@login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource created successfully!')
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'resources/resource_create.html', {'form': form})


@login_required
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES , instance=resource, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resource updated successfully!')
            return redirect('resource_list')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resources/resource_edite.html', {'form': form, 'resource': resource})



@login_required
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        return redirect('resource_list')
    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})


@login_required
def enrolled_course_list(request):
    user = request.user
    enrolled_courses = EnrolledCourse.objects.all()
    if user.is_student:
        student = get_object_or_404(Student, id=user.id)
        enrolled_courses = student.enrolled_student.all()
        return render(request, 'enrolled_courses/enrolled_course_list.html', {'enrolled_courses': enrolled_courses})
    return render(request, 'enrolled_courses/enrolled_course_list.html', {'enrolled_courses': enrolled_courses})


@login_required
def enrolled_course_detail(request, pk):
    enrolled_course = get_object_or_404(EnrolledCourse, pk=pk)
    return render(request, 'enrolled_courses/enrolled_course_detail.html', {'enrolled_course': enrolled_course})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student
  
    if student.is_student:
        if EnrolledCourse.objects.filter(student=student, course=course).exists():
            messages.info(request, 'You already enrolled this course!')
            return redirect('course_list')
        EnrolledCourse.objects.create(student=student, course=course)
        messages.success(request, 'You enrolled successfully.')
        return redirect('enrolled_course_list')  
    return redirect('course_list')

@login_required
def enrolled_course_create(request):
    if request.method == 'POST':
        form = EnrolledCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enrolled_course_list')
    else:
        form = EnrolledCourseForm()
    return render(request, 'enrolled_courses/enrolled_course_form.html', {'form': form})


@login_required
def enrolled_course_edit(request, pk):
    enrolled_course = get_object_or_404(EnrolledCourse, pk=pk)
    if request.method == 'POST':
        form = EnrolledCourseForm(request.POST, instance=enrolled_course)
        if form.is_valid():
            form.save()
            return redirect('enrolled_course_list')
    else:
        form = EnrolledCourseForm(instance=enrolled_course)
    return render(request, 'enrolled_courses/enrolled_course_form.html', {'form': form})


@login_required
def enrolled_course_delete(request, pk):
    enrolled_course = get_object_or_404(EnrolledCourse, pk=pk)
    if request.method == 'POST':
        enrolled_course.delete()
        return redirect('enrolled_course_list')
    return render(request, 'enrolled_courses/enrolled_course_confirm_delete.html', {'enrolled_course': enrolled_course})


@login_required
def discussion_list(request):
    user = request.user
    discussions = None
    if user.is_superuser:
        discussions = Discussion.objects.all()
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            discussions = Discussion.objects.filter(course__school=school)
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        discussions = Discussion.objects.filter(course__professors=professor)
    elif user.is_student:
        student = get_object_or_404(Student, id=user.id)
        discussions = Discussion.objects.filter(course__in=student.enrolled_student.values('course'))
    return render(request, 'discussions/discussion_list.html', {'discussions': discussions})


# @login_required
# def discussion_detail(request, pk):
#     discussion = get_object_or_404(Discussion, pk=pk)
#     return render(request, 'discussions/discussion_detail.html', {'discussion': discussion})

@login_required
def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    comments = discussion.comments.filter(parent__isnull=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.discussion = discussion
            new_comment.author = request.user
            if 'parent' in request.POST:
                parent_id = request.POST.get('parent')
                new_comment.parent = Comment.objects.get(id=parent_id)
            new_comment.save()
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'discussions/discussion_detail.html', {
        'discussion': discussion,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })


@login_required
def discussion_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.course = course
            discussion.starter = request.user
            discussion.save()
            messages.success(request, 'Discussion created successfully!')
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm()
    return render(request, 'discussions/discussion_create.html', {'form': form, 'course': course})
   


@login_required
def discussion_edit(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discussion updated successfully!')
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm(instance=discussion)
    return render(request, 'discussions/discussion_edit.html', {'form': form, 'discussion': discussion})


@login_required
def discussion_delete(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.method == 'POST':
        discussion.delete()
        messages.success(request, 'Discussion deleted successfully!')
        return redirect('discussion_detail', pk=discussion.pk)
    return render(request, 'discussions/discussion_confirm_delete.html', {'discussion': discussion})



@login_required
def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'comments/comment_list.html', {'comments': comments})


@login_required
def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    return render(request, 'comments/comment_detail.html', {'comment': comment})


@login_required
def comment_create(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment created successfully!')
            return redirect('comment_list')
    else:
        form = CommentForm()
    return render(request, 'comments/comment_form.html', {'form': form})


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    discussions = Discussion.objects.filter(comments=comment)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('discussion_detail', pk=discussions.first().pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comments/comment_edit.html', {'form': form, 'comment': comment, 'discussions': discussions})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    discussion = Discussion.objects.filter(comments=comment).first()
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('discussion_detail', pk=discussion.pk)
    return render(request, 'comments/comment_confirm_delete.html', {'comment': comment, 'discussion': discussion})


@login_required
@admin_or_superuser_or_profeesor_or_student_required
def profile(request):
    user = request.user
    if user.is_superuser:
        superuser_avatar = Profile.objects.filter(user=user)
        return render(request, 'profiles/profile.html', {'user': user, 'superuser_avatar': superuser_avatar})
    elif user.is_professor:
        course_taught = Course.objects.filter(professors=user)
        professor_avatar = Profile.objects.filter(user=user)
        return render(request, 'profiles/profile.html', {'user': user, 'course_taught': course_taught, 'professor_avatar': professor_avatar})
    elif user.is_student:
        student = get_object_or_404(Student, id=user.id)
        enrolled_courses = student.enrolled_student.all()
        student_avatar = Profile.objects.filter(user=user)
        return render(request, 'profiles/profile.html', {'user': user, 'student_avatar': student_avatar, 'enrolled_courses': enrolled_courses})
    elif user.is_admin:
        admin_avatar = Profile.objects.filter(user=user)
        return render(request, 'profiles/profile.html', {'user': user, 'admin_avatar': admin_avatar})
    else:
        messages.error(request, 'Profile does not exist!')
    return render(request, 'profiles/profile.html')

@login_required
def profile_by_id(request, pk):
    user = None
    course_taught = []
    professor_avatar = []
    enrolled_courses = []
    student_avatar = []

    try:
        # Try to get a professor first
        user = Professor.objects.get(id=pk)
        course_taught = Course.objects.filter(professors=user)
        professor_avatar = Profile.objects.filter(user=user)
    except Professor.DoesNotExist:
        try:
            # If not a professor, try to get a student
            user = Student.objects.get(id=pk)
            enrolled_courses = user.enrolled_student.all()
            student_avatar = Profile.objects.filter(user=user)
        except Student.DoesNotExist:
            messages.error(request, 'Profile does not exist!')
            return render(request, 'profiles/profile_by_id.html')

    return render(request, 'profiles/profile_by_id.html', {
        'user': user,
        'course_taught': course_taught,
        'professor_avatar': professor_avatar,
        'enrolled_courses': enrolled_courses,
        'student_avatar': student_avatar
    })

@login_required
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profiles/profile_list.html', {'profiles': profiles})


@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'profiles/profile_detail.html', {'profile': profile})


@login_required
def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = ProfileForm()
    return render(request, 'profiles/profile_form.html', {'form': form})


@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'profile updated')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile_form.html', {'form': form})


@login_required
def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('profile_list')
    return render(request, 'profiles/profile_confirm_delete.html', {'profile': profile})


@login_required
def zoom_meeting_list(request):
    zoom_meetings = ZoomMeeting.objects.all()
    return render(request, 'zoom_meetings/zoom_meeting_list.html', {'zoom_meetings': zoom_meetings})


@login_required
def zoom_meeting_detail(request, pk):
    zoom_meeting = get_object_or_404(ZoomMeeting, pk=pk)
    return render(request, 'zoom_meetings/zoom_meeting_detail.html', {'zoom_meeting': zoom_meeting})


@login_required
def zoom_meeting_create(request):
    if request.method == 'POST':
        form = ZoomMeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zoom_meeting_list')
    else:
        form = ZoomMeetingForm()
    return render(request, 'zoom_meetings/zoom_meeting_form.html', {'form': form})


@login_required
def zoom_meeting_edit(request, pk):
    zoom_meeting = get_object_or_404(ZoomMeeting, pk=pk)
    if request.method == 'POST':
        form = ZoomMeetingForm(request.POST, instance=zoom_meeting)
        if form.is_valid():
            form.save()
            return redirect('zoom_meeting_list')
    else:
        form = ZoomMeetingForm(instance=zoom_meeting)
    return render(request, 'zoom_meetings/zoom_meeting_form.html', {'form': form})


@login_required
def zoom_meeting_delete(request, pk):
    zoom_meeting = get_object_or_404(ZoomMeeting, pk=pk)
    if request.method == 'POST':
        zoom_meeting.delete()
        return redirect('zoom_meeting_list')
    return render(request, 'zoom_meetings/zoom_meeting_confirm_delete.html', {'zoom_meeting': zoom_meeting})


@login_required
def message_list(request):
    user = request.user
    messages_list = None
    if user.is_superuser:
        messages_list = Message.objects.all()
    else:
        messages_list = Message.objects.filter(sender=user)
    return render(request, 'messages/message_list.html', {'messages_list': messages_list})


@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'messages/message_detail.html', {'message': message})


# @login_required
# def message_create(request):
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('message_list')
#     else:
#         form = MessageForm()
#     return render(request, 'messages/message_form.html', {'form': form})


@login_required
def message_edit(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message, request=request)
        if form.is_valid():
            message = form.save(commit=False)
            students = form.cleaned_data.get('students')
            professors = form.cleaned_data.get('professors')
            admins = form.cleaned_data.get('admins')

            recipients = list(students) + list(professors) + list(admins)
            message.recipients.set(recipients)
            message.save()
            messages.success(request, 'Message updated successfully!')
            return redirect('message_list')
    else:
        form = MessageForm(instance=message, request=request)
    return render(request, 'messages/message_edit.html', {'form': form, 'message': message})


@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully!')
        return redirect('message_list')
    return render(request, 'messages/message_confirm_delete.html', {'message': message})



@login_required
def student_list(request):
    user = request.user
    
    # Check if the user is an admin
    if user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        school = School.objects.get(admin_school=admin)
        
        # Get students enrolled in courses that belong to the admin's school
        students = Student.objects.filter(school=school).distinct()

        # Retrieve profile pictures for students
        student_avatars = {student.id: Profile.objects.filter(user=student).first() for student in students}

        students_with_avatars = [
                {
                    'student': student,
                    'telephone': student_avatars[student.id].telephone if student.id in student_avatars else 'N/A',
                    'location': student_avatars[student.id].location if student.id in student_avatars else 'N/A'
                }
                for student in students
            ]
            
        return render(request, 'students/student_list.html', {
            'students_with_avatars': students_with_avatars
        })
        
    elif user.is_superuser:
        # Get all students
        students = Student.objects.all()
        student_avatars = {student.id: Profile.objects.filter(user=student).first() for student in students}

        students_with_avatars = [
            {
                'student': student,
                'telephone': student_avatars[student.id].telephone if student.id in student_avatars else 'N/A',
                'location': student_avatars[student.id].location if student.id in student_avatars else 'N/A'
            }
            for student in students
        ]
    
        return render(request, 'students/student_list.html', {'students': students, 'students_with_avatars': students_with_avatars})
    else:
        return redirect('home')  # Handle the case where the user is not an admin


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_edite.html', {'form': form})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})




@login_required
def professor_list(request):
    user = request.user
    
    # Check if the user is a superuser
    if user.is_superuser:
        professors = Professor.objects.all()
    else:
        # Check if the user is an admin
        admin = get_object_or_404(Admin, id=user.id)
        school = School.objects.filter(admin_school=admin).first()  
        professors = Professor.objects.filter(school=school).distinct()
    
    # Retrieve profile pictures for professors
    professor_avatars = {professor.id: Profile.objects.filter(user=professor).first() for professor in professors}
    professors_with_avatars = [
            {
                'professor': professor,
                'telephone': professor_avatars[professor.id].telephone if professor.id in professor_avatars else 'N/A',
                'location': professor_avatars[professor.id].location if professor.id in professor_avatars else 'N/A'
            }
            for professor in professors
        ]
        
    return render(request, 'professors/professor_list.html', {
        'professors_with_avatars': professors_with_avatars
    })

@login_required
def professor_detail(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    return render(request, 'professors/professor_detail.html', {'professor': professor})


@login_required
def account_setting(request, pk):
    user = request.user
    if user.is_professor:
        professor = get_object_or_404(Professor, pk=pk)
        form = ProfessorForm(instance=professor, user=user)
        if request.method == 'POST':
            form = ProfessorForm(request.POST, instance=professor)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account is updated successfuly.')
                return redirect('profile')
            messages.error(request, 'invalid form')  
        return render(request, 'registration/account_sitting.html', {'form': form})
    
    elif user.is_superuser:
        superuser = get_object_or_404(BaseUser, pk=pk)
        form = BaseUserForm(instance=superuser)
        if request.method == 'POST':
            form = BaseUserForm(request.POST, instance=superuser)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account is updated successfuly.')
                return redirect('home')
            messages.error(request, 'invalid form')  
        return render(request, 'registration/account_sitting.html', {'form': form})
    
    elif user.is_admin:
        admin = get_object_or_404(Admin, pk=pk)
        form = AdminForm(instance=admin, user=user)
        if request.method == 'POST':
            form = AdminForm(request.POST, instance=admin)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account is updated successfuly.')
                return redirect('profile')
            messages.error(request, 'invalid form')  
        return render(request, 'registration/account_sitting.html', {'form': form})
            
    elif user.is_student:
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(instance=student, user=user)
        if request.method == 'POST':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account is updated successfuly.')
                return redirect('profile')
            messages.error(request, 'invalid student form')  
        return render(request, 'registration/account_sitting.html', {'form': form})
    else:
        messages.error(request, 'No user is login')
        return redirect('home')

@login_required
def professor_edit(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor updated successfully!')
            return redirect('professor_list')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'professors/professor_edite.html', {'form': form})


@login_required
def professor_delete(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        professor.delete()
        messages.success(request, 'Professor deleted successfully!')
        return redirect('professor_list')
    return render(request, 'professors/professor_confirm_delete.html', {'professor': professor})




@login_required
def admin_list(request):
    admins = Admin.objects.all()
    return render(request, 'admins/admin_list.html', {'admins': admins})


@login_required
def admin_detail(request, pk):
    admin = get_object_or_404(Admin, pk=pk)
    return render(request, 'admins/admin_detail.html', {'admin': admin})


@login_required
def admin_edit(request, pk):
    admin = get_object_or_404(Admin, pk=pk)
    if request.method == 'POST':
        form = AdminForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('admin_list')
    else:
        form = AdminForm(instance=admin)
    return render(request, 'admins/admin_form.html', {'form': form})


@login_required
def admin_delete(request, pk):
    admin = get_object_or_404(Admin, pk=pk)
    if request.method == 'POST':
        admin.delete()
        return redirect('admin_list')
    return render(request, 'admins/admin_confirm_delete.html', {'admin': admin})


@login_required
def search(request):
    return SearchView.as_view()(request)





# views.py
def error_404(request, exception):
    return render(request, '505_404.html', status=404)


