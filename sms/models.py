from django.db import models

# Create your models here.

class Sender_User(models.Model):
    notice_id = models.CharField(blank=False, null=False, primary_key=True, unique=True, max_length=200)
    notice_ps = models.CharField(max_length=200, blank=False, null=False)
    def __str__(self):
        return str('%s' % (self.notice_id))



class Notice(models.Model):
    notice_date = models.DateTimeField('date',primary_key=True )
    notice_title =  models.CharField(max_length=200)
    notice_text = models.CharField(max_length=1200)
    notice_id= models.ForeignKey(Sender_User, on_delete=models.CASCADE)
    notice_ps= models.CharField(max_length=200,blank=False, null=False)

    def __str__(self):
        return str('%s' % (self.notice_date))





class Message_User(models.Model):

    user_phoneNumber = models.CharField(max_length=200,primary_key=True , unique=True)
    user_name =  models.CharField(max_length=200)
    user_group = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str('%s %s' % (self.user_phoneNumber, self.user_name))



class Message(models.Model):
    individual_notice_text = models.CharField(max_length=1200)
    notice_url = models.CharField(max_length=600,primary_key=True , unique=True)
    notice_date  =models.ForeignKey(Notice, on_delete=models.CASCADE)
    isConfirmbyReceiver =models.BooleanField(default=False)
    user_phoneNumber =models.ForeignKey(Message_User, on_delete=models.CASCADE)
    notice_id=models.ForeignKey(Sender_User, on_delete=models.CASCADE)
    def __str__(self):
        return str('%s %s ' % (self.user_phoneNumber, self.notice_id))







# https://docs.djangoproject.com/ko/3.1/intro/tutorial02/
# python manage.py makemigrations sms
#  python manage.py migrate
# python manage.py createsuperuser
