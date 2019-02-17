from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """注册用新的model，通过user字段对User表一一对应"""
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(blank=True, max_length=20, null=True)
    
    def __str__(self):
        return 'User {}'.format(self.user.username)

class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return 'User {}'.format(self.user.username)

