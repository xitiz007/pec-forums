from django.shortcuts import redirect, get_object_or_404, render
from .models import Faculty
from forums.models import Question
from django.contrib import messages

def is_user_authenticated(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('warning')
        
        return view_function(request, *args, **kwargs)
    
    return wrapper_function

def is_user_authenticated_faculty(view_function):
    def wrapper_function(request, faculty_id, *args, **kwargs):
        faculty = get_object_or_404(Faculty, id= faculty_id)
        if faculty == request.user.userprofile.faculty:
            return view_function(request, faculty_id, *args, **kwargs)
        else:
            message = "you can only view your faculty"
            messages.warning(request, message)
            return render(request, 'forums/error-message.html')

    return wrapper_function



