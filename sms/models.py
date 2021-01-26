from django.db import models

# Create your models here.

class Notice(models.Model):
    notice_date = models.DateTimeField('date')
    notice_title =  models.CharField(max_length=200)
    notice_key= models.IntegerField(blank=False, null=False ,primary_key=True , unique=True)


class Message_User(models.Model):

    user_phoneNumber = models.CharField(max_length=200,primary_key=True , unique=True)
    user_name =  models.CharField(max_length=200)
    user_group = models.CharField(max_length=50, blank=True, null=True)



class Message(models.Model):
    notice_text = models.CharField(max_length=600)
    notice_url = models.CharField(max_length=600,primary_key=True , unique=True)
    notice_key  =models.ForeignKey(Notice, on_delete=models.CASCADE)
    isConfirmbyReceiver =models.BooleanField(default=False)
    user_phoneNumber =models.ForeignKey(Message_User, on_delete=models.CASCADE)







# https://docs.djangoproject.com/ko/3.1/intro/tutorial02/
# python manage.py makemigrations sms
#  python manage.py migrate
# python manage.py createsuperuser
