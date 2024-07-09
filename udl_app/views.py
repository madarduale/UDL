from django.shortcuts import render, redirect
from .models import Message
# Create your views here.
import jwt
from .jaas_jwt import JaaSJwtBuilder
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from .searchs import SearchView
from collections import defaultdict
from django.db.models import Count
from .forms import (
    MessageForm, CourseForm, LectureForm,
    AssignmentForm, AssigmmentGradeForm, AssignmentSubmissionForm,
    QuizForm, QuizGradingForm, QuizSubmissionForm,
    ExamForm, ExamGradingForm, ExamSubmissionForm,
    QuestionForm, SchoolForm,
    choiceForm, ResourceForm, EnrolledCourseForm,
    DiscussionForm, CommentForm, ProfileForm,
    ZoomMeetingForm, AdminForm, ProfessorForm, StudentForm, BaseUserForm
)

from django.shortcuts import render, get_object_or_404, redirect
from .models import(
    Admin, Professor, Student, Course, Lecture, Grade,
    Assignment, AssignmentGrade, AssignmentSubmission,
    Quiz, QuizGrading, QuizSubmission,
    Exam, ExamGrading, ExamSubmission,
    Question, Choice, Resource, EnrolledCourse,
    Discussion, Comment, Profile, LectureProgress,
    School, Message, ZoomMeeting, BaseUser
) 

from .decorators import(
admin_required, professor_required, student_required, 
admin_or_professor_required, admin_or_professor_or_student_required, 
admin_or_superuser_required, superuser_required,
)


    


@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'udl_app/home.html')



def generate_jwt(user):
    jaas_jwt = JaaSJwtBuilder()
    private_key = settings.JWT_PRIVATE_KEY.strip() 

    token = jaas_jwt.withDefaults() \
        .withApiKey("vpaas-magic-cookie-943c0882125d4e38beba77d5b36093a7/45e73f") \
        .withUserName(user.username) \
        .withUserEmail(user.email) \
        .withModerator(user.is_staff) \
        .withAppID("vpaas-magic-cookie-943c0882125d4e38beba77d5b36093a7") \
        .withUserAvatar(user.profile.avatar.url if user.profile.avatar else '') \
        .signWith(private_key)

    return token



def jitsi_meet(request):
    # jwt_token = generate_jwt(request.user)
    jwt_token = generate_jwt(request.user)
    # decoded_token = jwt.decode(jwt_token, verify=False, algorithms=['RS256']) 
    decoded_token = jwt_token.decode("utf-8")

    print(decoded_token)
    # jwt_token2='eyJraWQiOiJ2cGFhcy1tYWdpYy1jb29raWUtOTQzYzA4ODIxMjVkNGUzOGJlYmE3N2Q1YjM2MDkzYTcvZWIwOWViLVNBTVBMRV9BUFAiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJqaXRzaSIsImlzcyI6ImNoYXQiLCJpYXQiOjE3MTQ4NTQyNTEsImV4cCI6MTcxNDg2MTQ1MSwibmJmIjoxNzE0ODU0MjQ2LCJzdWIiOiJ2cGFhcy1tYWdpYy1jb29raWUtOTQzYzA4ODIxMjVkNGUzOGJlYmE3N2Q1YjM2MDkzYTciLCJjb250ZXh0Ijp7ImZlYXR1cmVzIjp7ImxpdmVzdHJlYW1pbmciOnRydWUsIm91dGJvdW5kLWNhbGwiOnRydWUsInNpcC1vdXRib3VuZC1jYWxsIjpmYWxzZSwidHJhbnNjcmlwdGlvbiI6dHJ1ZSwicmVjb3JkaW5nIjp0cnVlfSwidXNlciI6eyJoaWRkZW4tZnJvbS1yZWNvcmRlciI6ZmFsc2UsIm1vZGVyYXRvciI6dHJ1ZSwibmFtZSI6Im1hZGFyZHVjYWFsZTk5ODgiLCJpZCI6ImF1dGgwfDY2MzVkNTc4NjFhOTRkZGMzNjA2NzU5NCIsImF2YXRhciI6IiIsImVtYWlsIjoibWFkYXJkdWNhYWxlOTk4OEBnbWFpbC5jb20ifX0sInJvb20iOiIqIn0.TzxGx5krRc0AM7xKo0F5iHb6vZoGngmjj8uO-F-wHE_VTg9qVL_HS0nPuANP35jaiyZqJakWv3P2KZwCyCc49tCTk8XOc7MuHj7vWetKTdao-Kj_IC9gZipX2peBCeGWOdZe2gWQ-Skj2GT6-h90sl_D6916rdYonoKZBTwzjOOympJNh3YKAQ4DIbmiV4K34vgg2bY6wFRCBnVL5g5fQAbcVwIOIVco7gvJjCgukXwkho-wCRHl8VWJgDQKVVhBA-pGvsHU7v41kKLGRxyz6QK9FOfWML0mQikL7G9tOkj3tm0KXlUQESfUnDQbCpToZbsF9kzbMZBRPlELWP4-Ug'
    return render(request, 'udl_app/jitsi_meet.html', {'jwt_token': decoded_token})



def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('inbox') 
    else:
        form = MessageForm()
    return render(request, 'udl_app/send_message.html', {'form': form})

def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user)
    jwt_token = generate_jwt(request.user)
    decoded_token = jwt_token.decode("utf-8")
    print(decoded_token)
    message_urls = []  
    for message in received_messages:
        if message.url:
            meeting_url = f'{message.url}?jwt={decoded_token}'
            message_urls.append((message, meeting_url))
    return render(request, 'udl_app/inbox.html', {'message_urls':message_urls})





@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

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
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@login_required
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
        return redirect('school_list')
    return render(request, 'schools/school_confirm_delete.html', {'school': school})


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
        lectures = Lecture.objects.all()
        grouped_by_course = defaultdict(list)
        for lecture in lectures:
            grouped_by_course[lecture.course].append(lecture)
        return render(request, 'lectures/lecture_list.html', {'lectures': lectures, 'grouped_by_course': dict(grouped_by_course),  'form': form}) 
    elif user.is_admin:
        admin = get_object_or_404(Admin, id=user.id)
        for school in admin.school.all():
            lectures = Lecture.objects.filter(course__school=school)
        grouped_by_course = defaultdict(list)
        for lecture in lectures:
            grouped_by_course[lecture.course].append(lecture)
        return render(request, 'lectures/lecture_list.html', {'lectures': lectures, 'grouped_by_course': dict(grouped_by_course), 'form': form}) 
    elif user.is_professor:
        professor = get_object_or_404(Professor, id=user.id)
        lectures = Lecture.objects.filter(course__professors=professor)
        grouped_by_course = defaultdict(list)
        for lecture in lectures:
            grouped_by_course[lecture.course].append(lecture)
        return render(request, 'lectures/lecture_list.html', {'lectures': lectures, 'grouped_by_course': dict(grouped_by_course), 'form': form})
    elif user.is_student:
        student = get_object_or_404(Student, id=user.id)
        enrolled_course = EnrolledCourse.objects.filter(student=student)
        lectures = Lecture.objects.filter(course__in=enrolled_course.values('course'))
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
def student__course_lectures(request, pk):
    student = get_object_or_404(Student, id=request.user.id)
    course = get_object_or_404(Course, pk=pk)
    lectures = Lecture.objects.filter(course=course)
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
    resource = Resource.objects.filter(lecture=lecture)
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
    if request.method == 'POST':
        assignment_create(request)
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
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments, 'form': form})


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
    assignment_submissions = AssignmentSubmission.objects.all()
    return render(request, 'assignment_submissions/assignment_submission_list.html', {'assignment_submissions': assignment_submissions})


@login_required
def assignment_submission_detail(request, pk):
    assignment_submission = get_object_or_404(AssignmentSubmission, pk=pk)
    return render(request, 'assignment_submissions/assignment_submission_detail.html', {'assignment_submission': assignment_submission})


@login_required
def assignment_submission_create(request):
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignment_submission_list')
    else:
        form = AssignmentSubmissionForm()
    return render(request, 'assignment_submissions/assignment_submission_form.html', {'form': form})


@login_required
def assignment_submission_edit(request, pk):
    assignment_submission = get_object_or_404(AssignmentSubmission, pk=pk)
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, instance=assignment_submission)
        if form.is_valid():
            form.save()
            return redirect('assignment_submission_list')
    else:
        form = AssignmentSubmissionForm(instance=assignment_submission)
    return render(request, 'assignment_submissions/assignment_submission_form.html', {'form': form})


@login_required
def assignment_submission_delete(request, pk):
    assignment_submission = get_object_or_404(AssignmentSubmission, pk=pk)
    if request.method == 'POST':
        assignment_submission.delete()
        return redirect('assignment_submission_list')
    return render(request, 'assignment_submissions/assignment_submission_confirm_delete.html', {'assignment_submission': assignment_submission})


@login_required
def assignment_grade_list(request):
    assignment_grades = AssignmentGrade.objects.all()
    return render(request, 'assignment_grades/assignment_grade_list.html', {'assignment_grades': assignment_grades})    


@login_required 
def assignment_grade_detail(request, pk):
    assignment_grade = get_object_or_404(AssignmentGrade, pk=pk)
    return render(request, 'assignment_grades/assignment_grade_detail.html', {'assignment_grade': assignment_grade})



@login_required
def assignment_grade_create(request):
    if request.method == 'POST':
        form = AssigmmentGradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignment_grade_list')
    else:
        form = AssigmmentGradeForm()

    return render(request, 'assignment_grades/assignment_grade_form.html', {'form': form})


@login_required
def assignment_grade_edit(request, pk):
    assignment_grade = get_object_or_404(AssignmentGrade, pk=pk)
    if request.method == 'POST':
        form = AssigmmentGradeForm(request.POST, instance=assignment_grade)
        if form.is_valid():
            form.save()
            return redirect('assignment_grade_list')
    else:
        form = AssigmmentGradeForm(instance=assignment_grade)
    return render(request, 'assignment_grades/assignment_grade_form.html', {'form': form})


@login_required
def assignment_grade_delete(request, pk):
    assignment_grade = get_object_or_404(AssignmentGrade, pk=pk)
    if request.method == 'POST':
        assignment_grade.delete()
        return redirect('assignment_grade_list')
    return render(request, 'assignment_grades/assignment_grade_confirm_delete.html', {'assignment_grade': assignment_grade})


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})  


@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})


@login_required
def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm()
    return render(request, 'quizzes/quiz_form.html', {'form': form})


@login_required
def quiz_edit(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quizzes/quiz_form.html', {'form': form})


@login_required
def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz_list')
    return render(request, 'quizzes/quiz_confirm_delete.html', {'quiz': quiz})


@login_required
def quiz_submission_list(request):
    quiz_submissions = QuizSubmission.objects.all()
    return render(request, 'quiz_submissions/quiz_submission_list.html', {'quiz_submissions': quiz_submissions})


@login_required
def quiz_submission_detail(request, pk):
    quiz_submission = get_object_or_404(QuizSubmission, pk=pk)
    return render(request, 'quiz_submissions/quiz_submission_detail.html', {'quiz_submission': quiz_submission})


@login_required
def quiz_submission_create(request):
    if request.method == 'POST':
        form = QuizSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_submission_list')
    else:
        form = QuizSubmissionForm()
    return render(request, 'quiz_submissions/quiz_submission_form.html', {'form': form})


@login_required
def quiz_submission_edit(request, pk):
    quiz_submission = get_object_or_404(QuizSubmission, pk=pk)
    if request.method == 'POST':
        form = QuizSubmissionForm(request.POST, instance=quiz_submission)
        if form.is_valid():
            form.save()
            return redirect('quiz_submission_list')
    else:
        form = QuizSubmissionForm(instance=quiz_submission)
    return render(request, 'quiz_submissions/quiz_submission_form.html', {'form': form})


@login_required
def quiz_submission_delete(request, pk):
    quiz_submission = get_object_or_404(QuizSubmission, pk=pk)
    if request.method == 'POST':
        quiz_submission.delete()
        return redirect('quiz_submission_list')
    return render(request, 'quiz_submissions/quiz_submission_confirm_delete.html', {'quiz_submission': quiz_submission})


@login_required
def quiz_grading_list(request):
    quiz_gradings = QuizGrading.objects.all()
    return render(request, 'quiz_gradings/quiz_grading_list.html', {'quiz_gradings': quiz_gradings})


@login_required
def quiz_grading_detail(request, pk):
    quiz_grading = get_object_or_404(QuizGrading, pk=pk)
    return render(request, 'quiz_gradings/quiz_grading_detail.html', {'quiz_grading': quiz_grading})


@login_required
def quiz_grading_create(request):
    if request.method == 'POST':
        form = QuizGradingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_grading_list')
    else:
        form = QuizGradingForm()
    return render(request, 'quiz_gradings/quiz_grading_form.html', {'form': form})


@login_required
def quiz_grading_edit(request, pk):
    quiz_grading = get_object_or_404(QuizGrading, pk=pk)
    if request.method == 'POST':
        form = QuizGradingForm(request.POST, instance=quiz_grading)
        if form.is_valid():
            form.save()
            return redirect('quiz_grading_list')
    else:
        form = QuizGradingForm(instance=quiz_grading)
    return render(request, 'quiz_gradings/quiz_grading_form.html', {'form': form})


@login_required
def quiz_grading_delete(request, pk):
    quiz_grading = get_object_or_404(QuizGrading, pk=pk)
    if request.method == 'POST':
        quiz_grading.delete()
        return redirect('quiz_grading_list')
    return render(request, 'quiz_gradings/quiz_grading_confirm_delete.html', {'quiz_grading': quiz_grading})


@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exam_list.html', {'exams': exams})


@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'exams/exam_detail.html', {'exam': exam})


@login_required
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'exams/exam_form.html', {'form': form})


@login_required
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'exams/exam_form.html', {'form': form})


@login_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        return redirect('exam_list')
    return render(request, 'exams/exam_confirm_delete.html', {'exam': exam})


@login_required
def exam_submission_list(request):
    exam_submissions = ExamSubmission.objects.all()
    return render(request, 'exam_submissions/exam_submission_list.html', {'exam_submissions': exam_submissions})



@login_required
def exam_submission_detail(request, pk):
    exam_submission = get_object_or_404(ExamSubmission, pk=pk)
    return render(request, 'exam_submissions/exam_submission_detail.html', {'exam_submission': exam_submission})


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
    exam_gradings = ExamGrading.objects.all()
    return render(request, 'exam_gradings/exam_grading_list.html', {'exam_gradings': exam_gradings})


@login_required
def exam_grading_detail(request, pk):
    exam_grading = get_object_or_404(ExamGrading, pk=pk)
    return render(request, 'exam_gradings/exam_grading_detail.html', {'exam_grading': exam_grading})


@login_required
def exam_grading_create(request):
    if request.method == 'POST':
        form = ExamGradingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_grading_list')
    else:
        form = ExamGradingForm()
    return render(request, 'exam_gradings/exam_grading_form.html', {'form': form})


@login_required
def exam_grading_edit(request, pk):
    exam_grading = get_object_or_404(ExamGrading, pk=pk)
    if request.method == 'POST':
        form = ExamGradingForm(request.POST, instance=exam_grading)
        if form.is_valid():
            form.save()
            return redirect('exam_grading_list')
    else:
        form = ExamGradingForm(instance=exam_grading)
    return render(request, 'exam_gradings/exam_grading_form.html', {'form': form})


@login_required
def exam_grading_delete(request, pk):
    exam_grading = get_object_or_404(ExamGrading, pk=pk)
    if request.method == 'POST':
        exam_grading.delete()
        return redirect('exam_grading_list')
    return render(request, 'exam_gradings/exam_grading_confirm_delete.html', {'exam_grading': exam_grading})


@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})


@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'questions/question_detail.html', {'question': question})


@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'questions/question_form.html', {'form': form})


@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'questions/question_form.html', {'form': form})


@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('question_list')
    return render(request, 'questions/question_confirm_delete.html', {'question': question})


@login_required
def choice_list(request):
    choices = Choice.objects.all()
    return render(request, 'choices/choice_list.html', {'choices': choices})


@login_required
def choice_detail(request, pk):
    choice = get_object_or_404(Choice, pk=pk)
    return render(request, 'choices/choice_detail.html', {'choice': choice})


@login_required
def choice_create(request):
    if request.method == 'POST':
        form = choiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('choice_list')
    else:
        form = choiceForm()
    return render(request, 'choices/choice_form.html', {'form': form})


@login_required
def choice_edit(request, pk):
    choice = get_object_or_404(Choice, pk=pk)
    if request.method == 'POST':
        form = choiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            return redirect('choice_list')
    else:
        form = choiceForm(instance=choice)
    return render(request, 'choices/choice_form.html', {'form': form})


@login_required
def choice_delete(request, pk):
    choice = get_object_or_404(Choice, pk=pk)
    if request.method == 'POST':
        choice.delete()
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
    discussions = Discussion.objects.all()
    return render(request, 'discussions/discussion_list.html', {'discussions': discussions})


@login_required
def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    return render(request, 'discussions/discussion_detail.html', {'discussion': discussion})


@login_required
def discussion_create(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discussion_list')
    else:
        form = DiscussionForm()
    return render(request, 'discussions/discussion_form.html', {'form': form})


@login_required
def discussion_edit(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            return redirect('discussion_list')
    else:
        form = DiscussionForm(instance=discussion)
    return render(request, 'discussions/discussion_form.html', {'form': form})


@login_required
def discussion_delete(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.method == 'POST':
        discussion.delete()
        return redirect('discussion_list')
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
            return redirect('comment_list')
    else:
        form = CommentForm()
    return render(request, 'comments/comment_form.html', {'form': form})


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comments/comment_form.html', {'form': form})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('comment_list')
    return render(request, 'comments/comment_confirm_delete.html', {'comment': comment})


@login_required
@admin_or_professor_or_student_required
def profile(request):
    user = request.user
    if user.is_professor:
        course_taught = Course.objects.filter(professors=user)
        # print('course_taught:', course_taught)
        professor_avatar = Profile.objects.filter(user=user)
        # print(professor_avatar.values())
        # messages.success(request, 'Profile  exists!')
        return render(request, 'registration/profile.html', {'user': user, 'course_taught': course_taught, 'professor_avatar': professor_avatar})
    elif user.is_student:
        student = get_object_or_404(Student, id=user.id)
        print('student:', student)
        enrolled_courses = student.enrolled_student.all()
        student_avatar = Profile.objects.filter(user=user)
        # messages.success(request, 'Profile  exists!')
        return render(request, 'registration/profile.html', {'user': user, 'student_avatar': student_avatar, 'enrolled_courses': enrolled_courses})
    elif user.is_admin:
        admin_avatar = Profile.objects.filter(user=user)
        # messages.success(request, 'Profile  exists!')
        return render(request, 'registration/profile.html', {'user': user, 'admin_avatar': admin_avatar})
    else:
        messages.error(request, 'Profile does not exist!')
    return render(request, 'registration/profile.html')

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
    messages = Message.objects.all()
    return render(request, 'messages/message_list.html', {'messages': messages})


@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'messages/message_detail.html', {'message': message})


@login_required
def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'messages/message_form.html', {'form': form})


@login_required
def message_edit(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    return render(request, 'messages/message_form.html', {'form': form})


@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('message_list')
    return render(request, 'messages/message_confirm_delete.html', {'message': message})




@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


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
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})





@login_required
def professor_list(request):
    professors = Professor.objects.all()
    return render(request, 'professors/professor_list.html', {'professors': professors})


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
            return redirect('professor_list')
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'professors/professor_form.html', {'form': form})


@login_required
def professor_delete(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        professor.delete()
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



from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Student Report")
    students = Student.objects.all()
    for i, student in enumerate(students):
        p.drawString(100, 700 - (i * 20), f"{student.first_name} {student.last_name}")
    p.showPage()
    p.save()
    return response
