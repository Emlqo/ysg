from django.db import models

# Create your models here.

class Message(models.Model):
    notice_text = models.CharField(max_length=600)
    notice_title =  models.CharField(max_length=200)



class User(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user_phoneNumber = models.CharField(max_length=200)
    user_name =  models.CharField(max_length=30)
    group =models.CharField(max_length=30)
    reception = models.IntegerField(default=0)

# https://docs.djangoproject.com/ko/3.1/intro/tutorial02/
# python manage.py makemigrations sms