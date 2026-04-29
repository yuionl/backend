from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user_app import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/', views.register),
    path('create_question/', views.create_question),
    path('get_question_list/', views.get_question_list),
    path('delete_questions/', views.delete_questions),
    path('get_question_detail/', views.get_question_detail),
    path('update_question/', views.update_question),
    path('create_course/', views.create_course),
    path('get_teacher_courses/', views.get_teacher_courses),
    path('get_course_students/', views.get_course_students),
    path('remove_course_student/', views.remove_course_student),
    path('join_course/', views.join_course),
    path('get_student_courses/', views.get_student_courses),
    path('exit_course/', views.exit_course),
    path('create_task/', views.create_task),
    path('get_teacher_tasks/', views.get_teacher_tasks),
    path('get_student_tasks/', views.get_student_tasks),
    path('get_student_task_status/', views.get_student_task_status),
    path('get_task_questions/', views.get_task_questions),
    path('submit_answer/', views.submit_answer),
    path('task_statistics/', views.task_statistics),
    path('get_essay_answers/', views.get_essay_answers),
    path('grade_essay/', views.grade_essay),
    path('get_student_answered_tasks/', views.get_student_answered_tasks),
    path('get_student_task_detail/', views.get_student_task_detail),
    path('upload_image/', views.upload_image),
    path('create_classroom/', views.create_classroom),
    path('get_active_classroom/', views.get_active_classroom),
    path('end_classroom/', views.end_classroom),
    path('get_classroom_detail/', views.get_classroom_detail),
    path('get_classroom_history/', views.get_classroom_history),
    path('create_task_in_classroom/', views.create_task_in_classroom),
    path('get_student_classroom/', views.get_student_classroom),
    path('get_student_performance/', views.get_student_performance),
    path('get_course_statistics/', views.get_course_statistics),
    path('get_classroom_history_stats/', views.get_classroom_history_stats),
    path('get_classroom_overview/', views.get_classroom_overview),
    path('get_question_analysis/', views.get_question_analysis),
    path('get_student_rank/', views.get_student_rank),
    path('get_classroom_rank/', views.get_classroom_rank),
    path('get_course_total_rank/', views.get_course_total_rank),
    path('get_teacher_student_profile/', views.get_teacher_student_profile),
    path('get_student_analysis/', views.get_student_analysis),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
