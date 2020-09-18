from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .decorators import is_user_authenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import AuthenticationForm, UserCreateForm, ChooseFaculty, ChangeUserProfileModel, ChangeUserModel
from .decorators import is_user_authenticated, is_user_authenticated_faculty
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Faculty

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.conf import settings
from .tokens import account_activation_token

from forums.models import Question, Answer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.models import Value
from django.db.models.functions import Concat
# Create your views here.

@is_user_authenticated
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request= request, email= email, password= password)
            if user is not None and not user.is_active:
                first_name = user.first_name
                last_name = user.last_name
                message = f'{first_name} {last_name} you havenot verified your email yet. Please check your email.'
                messages.warning(request, message)
            elif user is not None and user.is_active:
                login(request, user)
                first_name = user.first_name
                last_name = user.last_name
                message = f'welcome {first_name} {last_name}'
                messages.success(request, message)
                return redirect('home-page')
            else:
                message = 'invalid email/password'
                messages.warning(request, message)
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    
    return render(request, 'users/login.html', context)

@is_user_authenticated
def register_user(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        facutly_form = ChooseFaculty(request.POST)

        if form.is_valid() and facutly_form.is_valid():
            user = form.save(commit= False)
            user.is_active = False
            user.save()
            faculty = Faculty.objects.get(faculty_name= facutly_form.cleaned_data.get('faculty'))
            user_profile = UserProfile.objects.get(user= user)
            user_profile.faculty = faculty
            user_profile.save()

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            current_site = get_current_site(request)
            mail_subject = "Activate your PEC Forums account"
            message = render_to_string(
                'users/activate-user.html',
                {
                    'user' : user,
                    'domain' : current_site.domain,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token' : account_activation_token.make_token(user)
                }
            )

            send_email = EmailMessage(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            send_email.send()

            message = f"{first_name} {last_name} account created successfully, please check your email to verify your account"
            messages.success(request, message)
            return redirect('login')
    else:
        form = UserCreateForm()
        facutly_form = ChooseFaculty()

    context = {
        'form' : form,
        'facutly_form' : facutly_form
    }

    return render(request, 'users/register.html', context)

@login_required
def logout_user(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    message = f"{first_name} {last_name} your account successfully logged out"
    messages.success(request, message)
    logout(request)
    return redirect('home-page')

@login_required
def warning(request):
    return render(request, 'users/warning.html')

@is_user_authenticated
def activate(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk= user_id)
    except Exception:
        pass
    else:
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            message = f'{user.first_name} {user.last_name} your account is activated'
            messages.success(request, message)
            return redirect('login')
    
    return render(request, 'users/error.html')



def get_redundant(request):
    first_name = request.user.first_name
    last_name = request.user.last_name

    user_profile_model_form = ChangeUserProfileModel(initial= {
        'profile_picture' : request.user.userprofile.profile_picture,
        'faculty' : request.user.userprofile.faculty
    })

    user_model_form = ChangeUserModel(initial= {
        'first_name' : first_name,
        'last_name' : last_name
    })

    return user_profile_model_form, user_model_form

@login_required
def user_setting(request):

    if request.method == 'POST' and request.POST.get('form-type') == 'update-profile':

        user_profile_model_form = ChangeUserProfileModel(request.POST, request.FILES, instance= UserProfile.objects.get(user= request.user))
        user_model_form = ChangeUserModel(request.POST, instance= request.user)
        password_change_form = PasswordChangeForm(user= request.user)

        if user_profile_model_form.is_valid() and user_model_form.is_valid():
            user_profile_model_form.save()
            user_model_form.save()
            message = 'successfully updated your account'
            messages.success(request, message)
    
    elif request.method == 'POST' and request.POST.get('form-type') == 'password-change':

        user_profile_model_form, user_model_form = get_redundant(request)

        password_change_form = PasswordChangeForm(data= request.POST, user= request.user)
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            message = 'password changed successfully'
            messages.success(request, message)

    else:
        
        user_profile_model_form, user_model_form = get_redundant(request)

        password_change_form = PasswordChangeForm(user= request.user)

    context = {
        'user_profile_model_form' : user_profile_model_form,
        'user_model_form' : user_model_form,
        'password_change_form' : password_change_form
    }

    return render(request, 'users/setting.html', context)

@login_required
@is_user_authenticated_faculty
def faculties(request, faculty_id):
    faculty = Faculty.objects.get(id= faculty_id)
    students = faculty.userprofile_set.all()

    student_name = request.GET.get('name', None)

    if not student_name == "" and not student_name == None:
        student_name = str(student_name).strip()
        students = students.annotate(name=Concat('user__first_name', Value(' '), 'user__last_name')).filter(name__icontains= student_name)
        message = f'{len(students)} results found'
        messages.success(request, message)


    paginator = Paginator(students, 10)
    page_number = request.GET.get('page', 1)

    try:
        students = paginator.get_page(page_number)
    except PageNotAnInteger:
        students = paginator.get_page(1)
    except EmptyPage:
        students = paginator.get_page(paginator.num_pages)

    context= {
        'faculty' : faculty,
        'students' : students,
    }
    return render(request, 'users/faculty.html', context)

