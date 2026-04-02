from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponseForbidden
from django.db.models import Q

from .forms import StudentRegistrationForm
from .models import CustomUser


def home(request):
    return render(request, 'core/home.html')


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.is_approved = False
            user.is_active = True
            user.save()
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


@never_cache
@login_required
def dashboard_redirect(request):
    if request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')


@never_cache
@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('login')
    return render(request, 'core/student_dashboard.html')


@never_cache
@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('login')

    total_students = CustomUser.objects.filter(role='student').count()
    pending_count = CustomUser.objects.filter(
        role='student',
        is_approved=False,
        is_active=True
    ).count()
    active_count = CustomUser.objects.filter(
        role='student',
        is_approved=True,
        is_active=True
    ).count()
    deactivated_count = CustomUser.objects.filter(
        role='student',
        is_active=False
    ).count()

    context = {
        'total_students': total_students,
        'pending_count': pending_count,
        'active_count': active_count,
        'deactivated_count': deactivated_count,
    }

    return render(request, 'core/teacher_dashboard.html', context)


@never_cache
@login_required
def manage_students(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', 'all')

    students = CustomUser.objects.filter(role='student')

    if status_filter == 'pending':
        students = students.filter(is_approved=False, is_active=True)
    elif status_filter == 'approved':
        students = students.filter(is_approved=True, is_active=True)
    elif status_filter == 'deactivated':
        students = students.filter(is_active=False)

    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    total_students = CustomUser.objects.filter(role='student').count()
    pending_count = CustomUser.objects.filter(
        role='student',
        is_approved=False,
        is_active=True
    ).count()
    active_count = CustomUser.objects.filter(
        role='student',
        is_approved=True,
        is_active=True
    ).count()
    deactivated_count = CustomUser.objects.filter(
        role='student',
        is_active=False
    ).count()

    context = {
        'students': students,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_students': total_students,
        'pending_count': pending_count,
        'active_count': active_count,
        'deactivated_count': deactivated_count,
    }

    return render(request, 'core/manage_students.html', context)


@never_cache
@login_required
def approve_student(request, student_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    student = get_object_or_404(CustomUser, id=student_id, role='student')
    student.is_approved = True
    student.is_active = True
    student.save()

    return redirect('manage_students')


@never_cache
@login_required
def deactivate_student(request, student_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    student = get_object_or_404(CustomUser, id=student_id, role='student')
    student.is_active = False
    student.save()

    return redirect('manage_students')

@never_cache
@login_required
def reactivate_student(request, student_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    student = get_object_or_404(CustomUser, id=student_id, role='student')
    student.is_active = True
    student.save()

    return redirect('manage_students')


@never_cache
@login_required
def delete_student(request, student_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    student = get_object_or_404(CustomUser, id=student_id, role='student')

    if request.method == 'POST':
        student.delete()
        return redirect('manage_students')

    return render(request, 'core/confirm_delete_student.html', {'student': student})