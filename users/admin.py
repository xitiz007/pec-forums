from django.contrib import admin
from .models import UserProfile, Faculty

# Register your models here.
class FacultyAdmin(admin.ModelAdmin):
    readonly_fields = ['date_created']

admin.site.register(UserProfile)
admin.site.register(Faculty, FacultyAdmin)
