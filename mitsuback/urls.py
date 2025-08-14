from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('get-user/', views.get_user, name='get_user'),
    path('get-user-initials/', views.get_user_initials, name='get_user_initials'),
    path('select-winner/', views.select_winner_by_initial, name='select_winner_by_initial'),
    path('get-winners/', views.get_winners, name='get_winners'),
]       