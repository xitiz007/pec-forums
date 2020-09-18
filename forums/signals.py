from django.db.models.signals import post_save, pre_save
from .models import Answer, Like, UserNotification, Question

def add_notification_answer(sender, instance, created, **kwargs):
    if created and not instance.question.user == instance.user:
        UserNotification.objects.create(
            owner= instance.question.user,
            other= instance.user,
            question= instance.question,
            answer = instance
        )

def add_notification_like(sender, instance, created, **kwargs):
    if created and not instance.question.user == instance.user:
        UserNotification.objects.create(
            owner= instance.question.user,
            other= instance.user,
            question= instance.question,
            like = instance
        )


post_save.connect(add_notification_answer, sender= Answer)
post_save.connect(add_notification_like, sender= Like)

