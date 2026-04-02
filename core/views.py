from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import StudentRegistrationForm


def home(request):
    return render(request, 'core/home.html')


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
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
    return render(request, 'core/teacher_dashboard.html')