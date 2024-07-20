
from django.urls import path
from django.conf.urls import handler404, handler500
from django.shortcuts import render
from .views import (
   home,
   jitsi_meet,
   send_message,
   dashboard,
   inbox,

   course_create,
   course_detail,
   course_edit,
   course_list,
   course_delete,
   student__course_lectures,

   school_create,
   school_detail,
   school_edit,
   school_list,
   school_delete,

   semester_create,
   semester_detail,
   semester_edit,
   semester_list,
   semester_delete,


   lecture_create,
   lecture_detail,
   lecture_edit,
   lecture_list,
   lecture_delete,
   complete_lecture,
   incomplete_lecture,

   assignment_create,
   assignment_detail,
   assignment_edit,
   assignment_list,
   assignment_delete,

   assignment_submission_create,
   assignment_submission_detail,
   assignment_submission_edit,
   assignment_submission_list,
   assignment_submission_delete,

   assignment_grade_create,
   assignment_grade_detail,
   assignment_grade_edit,
   assignment_grade_list,
   assignment_grade_delete,

   exam_create,
   exam_detail,
   exam_edit,
   exam_list,
   exam_delete,

   exam_submission_create,
   exam_submission_detail,
   exam_submission_edit,
   exam_submission_list,
   exam_submission_delete,
   exam_submission_create_by_id,
   exam_submission_list_by_id,

   exam_grading_create,
   exam_grading_detail,
   exam_grading_edit,
   exam_grading_list,
   exam_grading_delete,

   question_create,
   question_detail,
   question_edit,
   question_list,
   question_delete,

   choice_create,
   choice_detail,
   choice_edit,
   choice_list,
   choice_delete,

   resource_create,
   resource_detail,
   resource_edit,
   resource_list,
   resource_delete,

   enroll_course,
   enrolled_course_create,
   enrolled_course_detail,
   enrolled_course_edit,
   enrolled_course_list,
   enrolled_course_delete,

   discussion_create,
   discussion_detail,
   discussion_edit,
   discussion_list,
   discussion_delete,

   comment_create,
   comment_detail,   
   comment_edit,
   comment_list,
   comment_delete,

   professor_detail,
   professor_edit,
   professor_list,
   professor_delete,

   zoom_meeting_create,
   zoom_meeting_detail,
   zoom_meeting_edit,
   zoom_meeting_list,
   zoom_meeting_delete,

   message_create,
   message_detail,
   message_edit,
   message_list,
   message_delete,
   unread_count,

 
   admin_detail,
   admin_edit,
   admin_list,
   admin_delete,

   student_detail,
   student_edit,
   student_list,
   student_delete,


   profile_detail,
   profile_edit,
   profile_list,
   profile_delete,
   profile,
   profile_by_id,

   search,
   account_setting,
   video_call,
   student_pdf,
   professor_pdf,
   professors_pdf,
   students_pdf,
   professor_video_call,
   error_404
)

def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {}, status=404 )

handler404 = custom_page_not_found_view

def custom_error_view(request):
    return render(request, "500.html", {}, status=500)

handler500 = custom_error_view


urlpatterns = [
   path('', home, name='home'),
   path('dashboard/', dashboard, name='dashboard'),
   path('meet/',jitsi_meet, name='jitsi_meeting'),
   path('send/', send_message, name='send_message'),
   path('inbox/', inbox, name='inbox'),
   path('messages/unread_count/', unread_count, name='unread_count'),
   path('search/', search, name='query'),
   path('account/<int:pk>/edit/', account_setting, name='account'),
   path('video-call/', video_call, name='video_call'),
   path('professor-video-call/<int:exam_id>/', professor_video_call, name='professor_video_call'),
   path('student/<int:student_id>/pdf/', student_pdf, name='student_pdf'),
   path('students/pdf/', students_pdf, name='students_pdf'),
   path('professor/<int:professor_id>/pdf/', professor_pdf, name='professor_pdf'),
   path('professors/pdf/', professors_pdf, name='professors_pdf'),


   path('course/create/', course_create, name='course_create'),
   path('course/<int:pk>/', course_detail, name='course_detail'),
   path('course/<int:pk>/edit/', course_edit, name='course_edit'),
   path('courses/', course_list, name='course_list'),
   path('course/<int:pk>/delete/', course_delete, name='course_delete'),
   path('student/<int:pk>/courses/', student__course_lectures, name='student__course_lectures'),

   path('school/create/', school_create, name='school_create'),
   path('school/<int:pk>/', school_detail, name='school_detail'),
   path('school/<int:pk>/edit/', school_edit, name='school_edit'),
   path('schools/', school_list, name='school_list'),
   path('school/<int:pk>/delete/', school_delete, name='school_delete'),


   path('semester/create/', semester_create, name='semester_create'),
   path('semester/<int:pk>/', semester_detail, name='semester_detail'),
   path('semester/<int:pk>/edit/', semester_edit, name='semester_edit'),
   path('semesters/', semester_list, name='semester_list'),
   path('semester/<int:pk>/delete/', semester_delete, name='semester_delete'),

   path('lecture/create/', lecture_create, name='lecture_create'),
   path('lecture/<int:pk>/', lecture_detail, name='lecture_detail'),
   path('lecture/<int:pk>/edit/', lecture_edit, name='lecture_edit'),
   path('lectures/', lecture_list, name='lecture_list'),
   path('lecture/<int:pk>/delete/', lecture_delete, name='lecture_delete'),
   path('lecture/<int:lecture_id>/complete/', complete_lecture, name='complete_lecture'),
   path('lecture/<int:lecture_id>/incomplete/', incomplete_lecture, name='incomplete_lecture'),

   path('assignment/create/', assignment_create, name='assignment_create'),
   path('assignment/<int:pk>/', assignment_detail, name='assignment_detail'),
   path('assignment/<int:pk>/edit/', assignment_edit, name='assignment_edit'),
   path('assignments/', assignment_list, name='assignment_list'),
   path('assignment/<int:pk>/delete/', assignment_delete, name='assignment_delete'),

   path('assignment_submission/create/', assignment_submission_create, name='assignment_submission_create'),
   path('assignment_submission/<int:pk>/', assignment_submission_detail, name='assignment_submission_detail'),
   path('assignment_submission/<int:pk>/edit/', assignment_submission_edit, name='assignment_submission_edit'),
   path('assignment_submissions/', assignment_submission_list, name='assignment_submission_list'),
   path('assignment_submission/<int:pk>/delete/', assignment_submission_delete, name='assignment_submission_delete'),

   path('assignment_grade/create/', assignment_grade_create, name='assignment_grade_create'),
   path('assignment_grade/<int:pk>/', assignment_grade_detail, name='assignment_grade_detail'),
   path('assignment_grade/<int:pk>/edit/', assignment_grade_edit, name='assignment_grade_edit'),
   path('assignment_grades/', assignment_grade_list, name='assignment_grade_list'),
   path('assignment_grade/<int:pk>/delete/', assignment_grade_delete, name='assignment_grade_delete'),

   path('exam/create/', exam_create, name='exam_create'),
   path('exam/<int:pk>/', exam_detail, name='exam_detail'),
   path('exam/<int:pk>/edit/', exam_edit, name='exam_edit'),
   path('exams/', exam_list, name='exam_list'),
   path('exam/<int:pk>/delete/', exam_delete, name='exam_delete'),

   path('exam/<int:pk>/submit/', exam_submission_create_by_id, name='exam_submission_create_by_id'),
   path('exam/<int:exam_id>/submissions/', exam_submission_list_by_id, name='exam_submission_list_by_id'),
   path('exam_submission/create/', exam_submission_create, name='exam_submission_create'),
   path('exam_submission/<int:pk>/', exam_submission_detail, name='exam_submission_detail'),
   path('exam_submission/<int:pk>/edit/', exam_submission_edit, name='exam_submission_edit'),   
   path('exam_submissions/', exam_submission_list, name='exam_submission_list'),
   path('exam_submission/<int:pk>/delete/', exam_submission_delete, name='exam_submission_delete'),

   path('exam_grading/create/', exam_grading_create, name='exam_grading_create'),
   path('exam_grading/<int:pk>/', exam_grading_detail, name='exam_grading_detail'),
   path('exam_grading/<int:pk>/edit/', exam_grading_edit, name='exam_grading_edit'),
   path('exam_gradings/', exam_grading_list, name='exam_grading_list'),
   path('exam_grading/<int:pk>/delete/', exam_grading_delete, name='exam_grading_delete'),

   path('question/create/', question_create, name='question_create'),
   path('question/<int:pk>/', question_detail, name='question_detail'),
   path('question/<int:pk>/edit/', question_edit, name='question_edit'),
   path('questions/', question_list, name='question_list'),
   path('question/<int:pk>/delete/', question_delete, name='question_delete'),

   path('choice/create/', choice_create, name='choice_create'),
   path('choice/<int:pk>/', choice_detail, name='choice_detail'),
   path('choice/<int:pk>/edit/', choice_edit, name='choice_edit'),
   path('choices/', choice_list, name='choice_list'),
   path('choice/<int:pk>/delete/', choice_delete, name='choice_delete'),

   path('resource/create/', resource_create, name='resource_create'),
   path('resource/<int:pk>/', resource_detail, name='resource_detail'),
   path('resource/<int:pk>/edit/', resource_edit, name='resource_edit'),
   path('resources/', resource_list, name='resource_list'),
   path('resource/<int:pk>/delete/', resource_delete, name='resource_delete'),

   path('enroll_course/<int:course_id>/', enroll_course, name='enroll_course'),
   path('enrolled_course/create/', enrolled_course_create, name='enrolled_course_create'),
   path('enrolled_course/<int:pk>/', enrolled_course_detail, name='enrolled_course_detail'), 
   path('enrolled_course/<int:pk>/edit/', enrolled_course_edit, name='enrolled_course_edit'),
   path('enrolled_courses/', enrolled_course_list, name='enrolled_course_list'),
   path('enrolled_course/<int:pk>/delete/', enrolled_course_delete, name='enrolled_course_delete'),

   path('discussion/create/', discussion_create, name='discussion_create'),
   path('discussion/<int:pk>/', discussion_detail, name='discussion_detail'),
   path('discussion/<int:pk>/edit/', discussion_edit, name='discussion_edit'),
   path('discussions/', discussion_list, name='discussion_list'),
   path('courses/<int:course_id>/create_discussion/', discussion_create, name='discussion_create'),
   path('discussion/<int:pk>/delete/', discussion_delete, name='discussion_delete'),

   path('comment/create/', comment_create, name='comment_create'),
   path('comment/<int:pk>/', comment_detail, name='comment_detail'),
   path('comment/<int:pk>/edit/', comment_edit, name='comment_edit'),
   path('comments/', comment_list, name='comment_list'),
   path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),


   path('professor/<int:pk>/', professor_detail, name='professor_detail'),
   path('professor/<int:pk>/edit/', professor_edit, name='professor_edit'),
   path('professors/', professor_list, name='professor_list'),
   path('professor/<int:pk>/delete/', professor_delete, name='professor_delete'),

   path('zoom_meeting/create/', zoom_meeting_create, name='zoom_meeting_create'),
   path('zoom_meeting/<int:pk>/', zoom_meeting_detail, name='zoom_meeting_detail'),
   path('zoom_meeting/<int:pk>/edit/', zoom_meeting_edit, name='zoom_meeting_edit'),
   path('zoom_meetings/', zoom_meeting_list, name='zoom_meeting_list'),
   path('zoom_meeting/<int:pk>/delete/', zoom_meeting_delete, name='zoom_meeting_delete'),

   path('message/create/', message_create, name='message_create'),
   path('message/<int:pk>/', message_detail, name='message_detail'),
   path('message/<int:pk>/edit/', message_edit, name='message_edit'),
   path('messages/', message_list, name='message_list'),
   path('message/<int:pk>/delete/', message_delete, name='message_delete'),

   
   path('admin/<int:pk>/', admin_detail, name='admin_detail'),
   path('admin/<int:pk>/edit/', admin_edit, name='admin_edit'),
   path('admins/', admin_list, name='admin_list'),
   path('admin/<int:pk>/delete/', admin_delete, name='admin_delete'),

   
   path('student/<int:pk>/', student_detail, name='student_detail'),
   path('student/<int:pk>/edit/', student_edit, name='student_edit'),
   path('students/', student_list, name='student_list'),
   path('student/<int:pk>/delete/', student_delete, name='student_delete'),

   path('profile/', profile, name='profile'),
   path('user/<int:pk>/', profile_by_id, name='profile_by_id'),
   path('profile/<int:pk>/', profile_detail, name='profile_detail'),
   path('profile/<int:pk>/edit/', profile_edit, name='profile_edit'),
   path('profiles/', profile_list, name='profile_list'),
   path('profile/<int:pk>/delete/', profile_delete, name='profile_delete'),


]
