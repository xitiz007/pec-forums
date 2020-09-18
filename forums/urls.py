from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= 'home-page'),
    path('view-question/<int:question_id>/', views.view_question, name='view-question'),
    path('delete-answer/<int:answer_id>/<int:question_id>/', views.delete_answer, name='delete-answer'),
    path('delete-question/<int:question_id>/', views.delete_question, name= 'delete-question'),
    path('edit-question/<int:question_id>/', views.edit_question, name='edit-question'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('like/<int:question_id>/', views.like_question, name='like-question'),
    path('clear-all-notification/', views.clear_all_notifications, name='clear-all-notification'),
    path('clear-notification/<int:page_number>/', views.clear_notification, name='clear-notification'),
]