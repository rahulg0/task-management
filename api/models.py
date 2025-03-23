from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.aws_lambda import lambda_handler
from dotenv import load_dotenv
load_dotenv()
import os


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    title=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    

@receiver(post_save, sender=Task)
def task_completion_notification(sender, instance, **kwargs):
    """Simulates an AWS Lambda function when a task is completed"""
    if instance.status == "completed" and os.getenv("AWS_LAMBDA_SIMULATION") == "True":
        event = {
            "task_id": instance.id,
            "task_title": instance.title,
            "user": instance.assigned_to.username if instance.assigned_to else "Unknown",
        }
        lambda_response = lambda_handler(event, None)
        print(lambda_response) 