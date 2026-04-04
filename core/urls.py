from django.urls import path
from . import views

urlpatterns = [

    # Core
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # -------------------------
    # STUDENTS
    # -------------------------
    path('teacher/students/', views.manage_students, name='manage_students'),
    path('teacher/students/<int:student_id>/approve/', views.approve_student, name='approve_student'),
    path('teacher/students/<int:student_id>/deactivate/', views.deactivate_student, name='deactivate_student'),
    path('teacher/students/<int:student_id>/reactivate/', views.reactivate_student, name='reactivate_student'),
    path('teacher/students/<int:student_id>/delete/', views.delete_student, name='delete_student'),

    # -------------------------
    # LESSONS & TOPICS
    # -------------------------
    path('teacher/lessons/', views.manage_lessons, name='manage_lessons'),

    path('teacher/topics/create/', views.create_topic, name='create_topic'),
    path('teacher/topics/<int:topic_id>/edit/', views.edit_topic, name='edit_topic'),
    path('teacher/topics/<int:topic_id>/delete/', views.delete_topic, name='delete_topic'),

    path('teacher/lessons/create/', views.create_lesson, name='create_lesson'),
    path('teacher/lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('teacher/lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),

    # -------------------------
    # QUIZZES
    # -------------------------
    path('teacher/quizzes/', views.manage_quizzes, name='manage_quizzes'),
    path('teacher/quizzes/create/', views.create_quiz, name='create_quiz'),
    path('teacher/quizzes/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('teacher/quizzes/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),

    # Questions
    path('teacher/quizzes/<int:quiz_id>/questions/add/', views.add_question, name='add_question'),

    # Question Types
    path('teacher/questions/<int:question_id>/choices/add/', views.add_choices, name='add_choices'),
    path('teacher/questions/<int:question_id>/true-false/add/', views.add_true_false_answer, name='add_true_false_answer'),


    # STUDENT LESSONS
    path('student/lessons/', views.student_lessons, name='student_lessons'),
    path('student/lessons/<int:lesson_id>/', views.student_lesson_detail, name='student_lesson_detail'),

    path('student/quizzes/', views.student_quizzes, name='student_quizzes'),
    path('student/quizzes/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('student/quizzes/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),

    path('student/progress/', views.student_progress, name='student_progress'),
    path('student/lessons/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
    
    path('teacher/performance-reports/', views.teacher_performance_reports, name='teacher_performance_reports'),




]