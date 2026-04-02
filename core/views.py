from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponseForbidden
from django.db.models import Q

from .models import CustomUser, Topic, Lesson, Quiz, Question, Choice
from .forms import (
    StudentRegistrationForm,
    TopicForm,
    LessonForm,
    QuizForm,
    QuestionForm,
)


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


# -------------------------
# STUDENT MANAGEMENT VIEWS
# -------------------------

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


# -------------------------
# MANAGE LESSONS VIEWS
# -------------------------

@never_cache
@login_required
def manage_lessons(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    search_query = request.GET.get('q', '')
    topic_filter = request.GET.get('topic', '')

    topics = Topic.objects.all().prefetch_related('lessons')

    if topic_filter:
        topics = topics.filter(id=topic_filter)

    if search_query:
        topics = topics.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(lessons__title__icontains=search_query) |
            Q(lessons__description__icontains=search_query) |
            Q(lessons__content__icontains=search_query)
        ).distinct()

    context = {
        'topics': topics,
        'all_topics': Topic.objects.all(),
        'search_query': search_query,
        'topic_filter': topic_filter,
    }

    return render(request, 'core/manage_lessons.html', context)


@never_cache
@login_required
def create_topic(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_lessons')
    else:
        form = TopicForm()

    return render(request, 'core/topic_form.html', {
        'form': form,
        'page_title': 'Create Topic'
    })


@never_cache
@login_required
def edit_topic(request, topic_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('manage_lessons')
    else:
        form = TopicForm(instance=topic)

    return render(request, 'core/topic_form.html', {
        'form': form,
        'page_title': 'Edit Topic'
    })


@never_cache
@login_required
def delete_topic(request, topic_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        topic.delete()
        return redirect('manage_lessons')

    return render(request, 'core/confirm_delete_topic.html', {'topic': topic})


@never_cache
@login_required
def create_lesson(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    initial_topic = request.GET.get('topic')

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_lessons')
    else:
        form = LessonForm(initial={'topic': initial_topic})

    return render(request, 'core/lesson_form.html', {
        'form': form,
        'page_title': 'Create Lesson'
    })


@never_cache
@login_required
def edit_lesson(request, lesson_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('manage_lessons')
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'core/lesson_form.html', {
        'form': form,
        'page_title': 'Edit Lesson'
    })


@never_cache
@login_required
def delete_lesson(request, lesson_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        lesson.delete()
        return redirect('manage_lessons')

    return render(request, 'core/confirm_delete_lesson.html', {'lesson': lesson})


# -------------------------
# MANAGE QUIZZES VIEWS
# -------------------------

@never_cache
@login_required
def manage_quizzes(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    search_query = request.GET.get('q', '')
    topic_filter = request.GET.get('topic', '')
    lesson_filter = request.GET.get('lesson', '')
    status_filter = request.GET.get('status', '')

    lessons = Lesson.objects.select_related('topic').prefetch_related('quizzes__questions')

    if topic_filter:
        lessons = lessons.filter(topic_id=topic_filter)

    if lesson_filter:
        lessons = lessons.filter(id=lesson_filter)

    if status_filter:
        lessons = lessons.filter(quizzes__status=status_filter)

    if search_query:
        lessons = lessons.filter(
            Q(title__icontains=search_query) |
            Q(topic__name__icontains=search_query) |
            Q(quizzes__title__icontains=search_query) |
            Q(quizzes__description__icontains=search_query) |
            Q(quizzes__questions__question_text__icontains=search_query)
        ).distinct()

    context = {
        'lessons': lessons.distinct(),
        'all_topics': Topic.objects.all(),
        'all_lessons': Lesson.objects.select_related('topic').all(),
        'search_query': search_query,
        'topic_filter': topic_filter,
        'lesson_filter': lesson_filter,
        'status_filter': status_filter,
    }

    return render(request, 'core/manage_quizzes.html', context)


@never_cache
@login_required
def create_quiz(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    initial_lesson = request.GET.get('lesson')

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_quizzes')
    else:
        form = QuizForm(initial={'lesson': initial_lesson})

    return render(request, 'core/quiz_form.html', {
        'form': form,
        'page_title': 'Create Quiz'
    })


@never_cache
@login_required
def edit_quiz(request, quiz_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('manage_quizzes')
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'core/quiz_form.html', {
        'form': form,
        'page_title': 'Edit Quiz'
    })


@never_cache
@login_required
def delete_quiz(request, quiz_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        quiz.delete()
        return redirect('manage_quizzes')

    return render(request, 'core/confirm_delete_quiz.html', {'quiz': quiz})


@never_cache
@login_required
def add_question(request, quiz_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()

            if question.question_type == 'mcq':
                return redirect('add_choices', question_id=question.id)
            elif question.question_type == 'tf':
                return redirect('add_true_false_answer', question_id=question.id)

            return redirect('manage_quizzes')
    else:
        form = QuestionForm()

    return render(request, 'core/question_form.html', {
        'form': form,
        'quiz': quiz,
        'page_title': 'Add Question'
    })


@never_cache
@login_required
def add_choices(request, question_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        Choice.objects.create(
            question=question,
            choice_text=request.POST.get('choice1'),
            is_correct=request.POST.get('correct_choice') == '1'
        )
        Choice.objects.create(
            question=question,
            choice_text=request.POST.get('choice2'),
            is_correct=request.POST.get('correct_choice') == '2'
        )
        Choice.objects.create(
            question=question,
            choice_text=request.POST.get('choice3'),
            is_correct=request.POST.get('correct_choice') == '3'
        )
        Choice.objects.create(
            question=question,
            choice_text=request.POST.get('choice4'),
            is_correct=request.POST.get('correct_choice') == '4'
        )
        return redirect('manage_quizzes')

    return render(request, 'core/add_choices.html', {'question': question})


@never_cache
@login_required
def add_true_false_answer(request, question_id):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")

    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        correct_answer = request.POST.get('correct_answer')

        Choice.objects.filter(question=question).delete()

        Choice.objects.create(
            question=question,
            choice_text='True',
            is_correct=(correct_answer == 'True')
        )
        Choice.objects.create(
            question=question,
            choice_text='False',
            is_correct=(correct_answer == 'False')
        )

        return redirect('manage_quizzes')

    return render(request, 'core/true_false_form.html', {'question': question})