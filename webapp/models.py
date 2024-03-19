from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager 




TASK_CHOICES = (
    ("HIGH","HIGH"),
    ("MEDIUM","MEDIUM"),
    ("LOW","LOW"),
)

# CREATE CUSTOME USER MODEL 
class CustomUserModel(AbstractUser):
    username    = None 
    email       = models.EmailField(unique=True)
    mobile_no   = models.CharField(max_length=200,null=True,blank=True)

    # DEFAULT UESERNAME & REQUIRED 
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    # DEFINING OUR NEW MANAGER 
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
    


# TASK 
class Task(models.Model):
    title       = models.CharField(max_length=200)
    creator     = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,null=True,blank=True,related_name='task')
    assigned_to = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='assigned_task')
    deadline    = models.DateTimeField()
    priority    = models.CharField(max_length=20,choices=TASK_CHOICES,default=0)
    description = models.TextField(null=True,blank=True)
    attachments = models.FileField(null=True,blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title) +'|'+ str(self.deadline)

# TASK TRACKING PROGRESS
class TaskProgress(models.Model):
    assignee        = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='task_progress')
    task            = models.OneToOneField('Task',on_delete=models.CASCADE,related_name='task_progress')
    completion_date = models.DateTimeField(null=True,blank=True)
    is_completed    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.task) +'|'+ str(self.is_completed)