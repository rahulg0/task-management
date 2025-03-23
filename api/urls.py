from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('tasks/', TaskView.as_view(), name='tasks'),
    path('get-users/', GetUsersView.as_view(), name='get-users'),
]