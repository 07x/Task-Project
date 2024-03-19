from django.urls import path

# VIEWS 
from .views import LoginAPI , RegistrationAPI , TaskCreation , TaskPerformance

urlpatterns = [

    path('login/',LoginAPI.as_view(),name='login'),
    path('register/',RegistrationAPI.as_view(),name='register'),
    path('task-creation/',TaskCreation.as_view(),name='task_creation'),
    path('task-performance/',TaskPerformance.as_view(),name='task-performance')

]
