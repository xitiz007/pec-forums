from django import template
from forums.models import Question
from django.contrib.auth.models import User
register = template.Library()

@register.simple_tag
def has_commented(question_id, user_id):
    question = Question.objects.get(id= question_id)
    user = User.objects.get(id= user_id)
    try:
        question.answer_set.get(user= user)
    except Exception:
        return False
    else:
        return True

@register.simple_tag
def has_liked(question_id, user_id):
    question = Question.objects.get(id= question_id)
    user = User.objects.get(id= user_id)
    try:
        question.like_set.get(user= user)
    except Exception:
        return False
    else:
        return True