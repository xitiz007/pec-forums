from django.contrib import admin
from .models import Question, Answer, Like, UserNotification
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['date_posted']

class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ['date_answered']

class UserNotificationAdmin(admin.ModelAdmin):
    readonly_fields = ['date']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Like)
admin.site.register(UserNotification, UserNotificationAdmin)