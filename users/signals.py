from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from .models import UserProfile
import os

def set_username_as_email(sender, instance, **kwargs):
    instance.username = instance.email

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user= instance)

def is_profile_picture_changed(sender, instance, **kwargs):
    if not instance._state.adding:
        old = UserProfile.objects.get(user= instance.user)
        old_picture_base_dir = os.path.basename(os.path.dirname(old.profile_picture.path))
        if not instance.profile_picture.path == old.profile_picture.path and old_picture_base_dir == 'profile_pictures':
            os.remove(old.profile_picture.path)


pre_save.connect(set_username_as_email, sender=User)

post_save.connect(create_user_profile, sender=User)

pre_save.connect(is_profile_picture_changed, sender= UserProfile)
