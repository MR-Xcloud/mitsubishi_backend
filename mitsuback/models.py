from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

class Register(models.Model):
    full_name = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    # employee_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class WinningList(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    initial = models.CharField(max_length=1)
    won_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.full_name} - {self.initial}"
    
    class Meta:
        unique_together = ['user', 'initial']  # Prevent duplicate wins for same initial