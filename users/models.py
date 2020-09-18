from forums import models as forum_model
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from allauth.socialaccount.models import SocialAccount

User._meta.get_field('email')._unique = True
# Create your models here.


class Faculty(models.Model):
    faculty_name = models.CharField(max_length= 100)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.faculty_name

    @property
    def get_total_students_count(self):
        return self.userprofile_set.all().count()

    @property
    def get_posted_questions_count(self):
        return self.question_set.all().count()

    @property
    def get_students(self):
        return self.userprofile_set.all().order_by('user__first_name', 'user__last_name')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    profile_picture = models.ImageField(default= 'user.png', upload_to = 'profile_pictures', null= True)
    faculty = models.ForeignKey(Faculty, on_delete= models.SET_NULL, null= True, blank= True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.profile_picture.path)
        if image.width > 300 or image.height > 300:
            to_resolution = (300, 300)
            image.thumbnail(to_resolution)
            image.save(self.profile_picture.path)

    @property
    def total_questioned(self):
        return forum_model.Question.objects.filter(user= self.user).count()

    @property
    def total_answered(self):
        return forum_model.Answer.objects.filter(user= self.user).distinct().count()

    @property
    def is_registered_from_social_account(self):
        try:
            SocialAccount.objects.get(user= self.user)
        except Exception:
            return False
        else:
            return True

    @property
    def has_user_set_faculty(self):
        return not self.faculty == None

