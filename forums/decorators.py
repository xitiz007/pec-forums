from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .models import Answer, Question
from django.contrib.auth.models import User
from .forms import CreateQuestion

def is_right_user_answer(view_function):
    def wrapper_function(request, answer_id, question_id, *args, **kwargs):
        answer = get_object_or_404(Answer, id= answer_id)
        if answer.user == request.user:
            return view_function(request, answer_id, question_id, *args, **kwargs)
        else:
            message = "you are not authorized user to delete the answer"
            messages.warning(request, message)
            return render(request, 'forums/error-message.html')
    
    return wrapper_function

def is_right_user_question(view_function):
    def wrapper_function(request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, id= question_id)
        if question.user == request.user:
            return view_function(request, question_id, *args, **kwargs)
        else:
            message = "you are not authorized user to delete the question"
            messages.warning(request, message)
            return render(request, 'forums/error-message.html')
    return wrapper_function

def is_user_authenticated_question(view_function):
    def wrapper_function(request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, id= question_id)
        if question.user == request.user:
            return view_function(request, question_id, *args, **kwargs)
        else:
            message = "you can only edit your questions"
            messages.warning(request, message)
            return render(request, 'forums/error-message.html')

    return wrapper_function

def is_right_user_view_question(view_function):
    def wrapper_function(request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, id= question_id)
        if question.faculty == request.user.userprofile.faculty or question.user == request.user:
            return view_function(request, question_id, *args, **kwargs)
        else:
            message = "you cannot view this question post"
            messages.warning(request, message)
            return render(request, 'forums/error-message.html')

    return wrapper_function

def can_view_profile(view_function):
    def wrapper_function(request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id= user_id)
        if user.userprofile.faculty == request.user.userprofile.faculty:
            return view_function(request, user_id, *args, **kwargs)
        else:
            message = "you cannot view other faculties user profile"
            messages.warning(request, message)
            return render(request, 'forums/error-message.html')

    return wrapper_function

def is_in_correct_faculty(view_function):
    def wrapper_function(request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, id=question_id)
        if question.faculty == request.user.userprofile.faculty or question.user == request.user:
            return view_function(request, question_id, *args, **kwargs)
        else:
            message = "you cannot view other faculties"
            messages.warning(request, message)
            return render(request, 'forums/error-message.html')

    return wrapper_function
