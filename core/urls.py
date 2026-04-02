from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    path('teacher/students/', views.manage_students, name='manage_students'),
    path('teacher/students/<int:student_id>/approve/', views.approve_student, name='approve_student'),
    path('teacher/students/<int:student_id>/deactivate/', views.deactivate_student, name='deactivate_student'),
    path('teacher/students/<int:student_id>/reactivate/', views.reactivate_student, name='reactivate_student'),
    path('teacher/students/<int:student_id>/delete/', views.delete_student, name='delete_student'),


]