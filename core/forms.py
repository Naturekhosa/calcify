from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Topic, Lesson,  Quiz, Question, Choice


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, label='Name')
    last_name = forms.CharField(max_length=150, label='Surname')
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if user.role == 'student' and not user.is_approved:
            raise ValidationError(
                "Your account is still pending approval.",
                code='not_approved',
            )
        
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['topic', 'title', 'description', 'content', 'video_link']


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['lesson', 'title', 'description', 'total_marks', 'time_limit', 'status']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'marks']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct']       