# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    platform = models.CharField(max_length=50)
    content = models.TextField()
    sentiment = models.CharField(max_length=10)
    purchase_intent = models.BooleanField()
    category = models.CharField(max_length=50, null=True, blank=True)
    entities = models.JSONField(null=True, blank=True)
    topics = models.JSONField(null=True, blank=True)
    keywords = models.JSONField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    trend_score = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.JSONField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    
