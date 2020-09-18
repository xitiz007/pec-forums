
from django.contrib import admin
from django.urls import path, include
from users import views as users_view

from django.contrib.auth.views import (PasswordResetView, 
PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forums.urls')),

    path('login/', users_view.login_user ,name= 'login'),
    path('register/', users_view.register_user, name= 'register'),
    path('logout/', users_view.logout_user, name='logout'),
    path('warning/',users_view.warning, name='warning' ),

    path('password-reset/', PasswordResetView.as_view(template_name= 'users/password-reset.html'), name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name= 'users/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name= 'users/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name= 'users/password-reset-complete.html'), name='password_reset_complete'),

    path('activate/<uidb64>/<token>/', users_view.activate, name='activate'),

    path('accounts/', include('allauth.urls')),

    path('setting/', users_view.user_setting, name='setting'),
    path('faculty/<int:faculty_id>/', users_view.faculties, name='faculty'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

