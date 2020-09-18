from django.db import models
from django.contrib.auth.models import User
from users.models import Faculty
from django import template

register = template.Library()

# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    question_title = models.TextField()
    faculty = models.ForeignKey(Faculty, on_delete= models.SET_NULL, null= True)
    date_posted = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Question, self).__init__(*args, **kwargs)
        self.__question_title = self.question_title
        self.__faculty = self.faculty
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if not self.question_title == self.__question_title or not self.faculty == self.__faculty:
            if not self.faculty == self.__faculty:
                answers = self.answer_set.all()
                answers.filter(question__faculty= self.__faculty).delete()
                likes = self.like_set.all()
                likes.filter(question__faculty= self.__faculty).delete()
            super(Question, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return f'{self.user.email} question {self.id}'
    
    @property
    def get_answered_count(self):
        return self.answer_set.all().count()

    @property
    def get_likes(self):
        return self.like_set.all().count()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    answer = models.TextField()
    date_answered = models.DateTimeField(auto_now_add= True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email} answer' 

class Like(models.Model):
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return f'{self.user.email} liked question number {self.question.id}'

class UserNotification(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name='owner')
    other = models.ForeignKey(User, on_delete= models.CASCADE, related_name='other')
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    like = models.ForeignKey(Like, on_delete= models.CASCADE, blank= True, null= True)
    answer= models.ForeignKey(Answer, on_delete= models.CASCADE, blank= True, null= True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def get_text(self):
        if self.like:
            return f' liked on your '
        else:
            return f' answered on your '

    def __str__(self):
        if self.like:
            return f'{self.other.email} liked {self.owner.email}\'s question id {self.question.id}'
        else:
            return f'{self.other.email} answered {self.owner.email}\'s question id {self.question.id}'


