from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferences = models.JSONField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Comment(models.Model):
    platform = models.CharField(max_length=50)
    content = models.TextField()
    sentiment = models.CharField(max_length=10)
    purchase_intent = models.BooleanField(default=False)
    category = models.CharField(max_length=50, null=True, blank=True)
    entities = models.JSONField(null=True, blank=True)
    topics = models.JSONField(null=True, blank=True)
    keywords = models.JSONField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    trend_score = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.platform} - {self.sentiment} by {self.user.username}"

class AnalysisHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    platform = models.CharField(max_length=50)
    positive_percent = models.FloatField()
    negative_percent = models.FloatField()
    purchase_intent_percent = models.FloatField()
    total_comments = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.platform} - {self.created_at}"
