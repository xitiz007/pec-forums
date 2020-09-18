from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .decorators import is_right_user_answer, is_right_user_question, is_user_authenticated_question, is_right_user_view_question, can_view_profile, is_in_correct_faculty
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CreateQuestion, CreateAnswer
from django.contrib import messages
from .models import Question, Answer, Like, UserNotification
from users.models import Faculty
from .filters import QuestionFilter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

@login_required
def home(request):
    if request.method == "POST":
        question_form = CreateQuestion(request.POST)
        if question_form.is_valid():
            form = question_form.save(commit= False)    
            form.user = request.user
            form.save()
            message = "your question posted successfully"
            messages.success(request, message)
            question_form = CreateQuestion(initial= {'faculty' : request.user.userprofile.faculty})

    else:
        user_faculty = request.user.userprofile.faculty
        question_form = CreateQuestion(initial = {'faculty' : user_faculty})

    questions = Question.objects.filter(faculty= request.user.userprofile.faculty).order_by('-date_posted')
    notifications = UserNotification.objects.filter(owner= request.user).order_by('-date')

    search = request.GET.get('search', None)
    if not search == "" and not search == None:
        search = str(search).strip()
        questions = questions.filter(question_title__icontains= search)
        message = f"{len(questions)} results found"
        messages.success(request, message)
        
    paginator = Paginator(questions, 5)
    paginator_notification = Paginator(notifications, 5)

    page_number = request.GET.get('page', 1)
    notification_page_number = request.GET.get('notification_page_number', 1)
    
    try:
        questions = paginator.get_page(page_number)
    except PageNotAnInteger:
        questions = paginator.get_page(1)
    except EmptyPage:
        questions = paginator.get_page(paginator.num_pages)

    try:
        notifications = paginator_notification.get_page(notification_page_number)
    except PageNotAnInteger:
        notifications = paginator_notification.get_page(1)
    except EmptyPage:
        notifications = paginator_notification.get_page(paginator_notification.num_pages)

    context = {
        'question_form' : question_form,
        'questions' : questions,
        'notifications' : notifications,
    }
    return render(request, 'forums/index.html', context)

@login_required
@can_view_profile
def user_profile(request, user_id):
    given_user = User.objects.get(id= user_id)
    if given_user == request.user:
        questions = Question.objects.filter(user= request.user).order_by('-date_posted')
        filter_form = QuestionFilter(request.GET, queryset= questions)
        questions = filter_form.qs

        if questions.count() == 0:
            if request.GET.get('faculty') == None or request.GET.get('faculty') == '':
                message = "you have not posted any questions yet"
            elif request.GET.get('faculty').isdigit():
                faculty = get_object_or_404(Faculty, id= request.GET.get('faculty'))
                message = f"you have not posted any questions in {faculty.faculty_name}"
            messages.warning(request, message)
    else:
        filter_form = None
        questions = Question.objects.filter(user= given_user, faculty= given_user.userprofile.faculty)
        if questions.count() == 0:
            message = f"{given_user.first_name} {given_user.last_name} has not posted any questions yet"
            messages.warning(request, message)

    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page', 1)

    try:
        questions = paginator.get_page(page_number)
    except PageNotAnInteger:
        questions = paginator.get_page(1)
    except EmptyPage:
        questions = paginator.get_page(paginator.num_pages)

    context = {
        'questions' : questions,
        'filter_form' : filter_form,
        'given_user' : given_user,
    }
    return render(request, 'forums/profile.html', context)

@login_required
@is_right_user_view_question
def view_question(request, question_id):
    question = Question.objects.get(id= question_id)

    if request.method == "POST":
        answer_form = CreateAnswer(request.POST)
        if answer_form.is_valid():
            answer_form = answer_form.save(commit= False)
            answer_form.user = request.user
            answer_form.question = question
            answer_form.save()
            answer_form = CreateAnswer()

    else:
        answer_form = CreateAnswer()

    answers = Answer.objects.filter(question= question).order_by('date_answered')
    likes = Like.objects.filter(question= question).order_by('user__first_name', 'user__last_name')

    paginator = Paginator(answers, 5)
    like_paginator = Paginator(likes, 10)

    page_number = request.GET.get('page', 1)
    like_page_number = request.GET.get('like_page_number', 1)

    try:
        answers = paginator.get_page(page_number)
    except PageNotAnInteger:
        answers = paginator.get_page(1)
    except EmptyPage:
        answers = paginator.get_page(paginator.num_pages)

    try:
        likes = like_paginator.get_page(like_page_number)
    except PageNotAnInteger:
        likes = like_paginator.get_page(1)
    except EmptyPage:
        likes = like_paginator.get_page(like_page_number.num_pages)

    context = {
        'question' : question,
        'answer_form' : answer_form,
        'answers' : answers,
        'likes' : likes
    }
    return render(request, 'forums/view-question.html', context)

@login_required
@is_right_user_answer
def delete_answer(request, answer_id, question_id):
    answer = Answer.objects.get(id= answer_id)
    answer.delete()
    return redirect('view-question', question_id)  

@login_required
@is_right_user_question
def delete_question(request, question_id):
    context = {

    }
    if request.method == "POST":
        question = Question.objects.get(id= question_id)
        question.delete()
        return redirect('profile', request.user.id)
    return render(request, 'forums/confirmation.html', context)


@login_required
@is_user_authenticated_question
def edit_question(request, question_id):
    question = Question.objects.get(id= question_id)
    if request.method == "POST":
        question_form = CreateQuestion(request.POST, instance= question)
        if question_form.is_valid():
            question_form_new = question_form.save(commit= False)
            question_form_new.edited = True
            question_form_new.save()

            message = "successfully saved question"
            messages.success(request, message)
    else:
        question_form = CreateQuestion(initial= {
            'question_title' : question.question_title,
            'faculty' : question.faculty
        })
    context = {
        'question_form' : question_form
    }
    return render(request, 'forums/edit-question.html', context)

@login_required
@is_in_correct_faculty
def like_question(request, question_id):
    question = Question.objects.get(id= question_id)
    try:
        like_question = question.like_set.get(user= request.user)
    except Exception:
        Like.objects.create(
            question= question,
            user= request.user
        )
    else:
        like_question.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def clear_all_notifications(request):
    try:
        UserNotification.objects.filter(owner= request.user).delete()
    except Exception:
        pass

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def clear_notification(request, page_number):
    try:
        notifications = UserNotification.objects.filter(owner= request.user)
    except Exception:
        pass
    else:
        starting_index = (page_number -1) * 5
        if starting_index >= 0:
            notifications = notifications[starting_index : starting_index + 5]
            for notification in notifications:
                notification.delete()

    return redirect(request.META.get('HTTP_REFERER'))