
from django.db import models

# Create your models here.

class Sender_User(models.Model):
    id = models.CharField(blank=False, null=False, primary_key=True, unique=True, max_length=200)
    ps = models.CharField(max_length=200, blank=False, null=False)
    aptNm = models.CharField(max_length=200, blank=True, null=True)
    complexNm= models.CharField(max_length=200, blank=True, null=True)
    villageNm =models.CharField(max_length=200, blank=True, null=True)
    aptAddress=models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return str('%s' % (self.id))



class Notice(models.Model):
    notice_date = models.CharField(max_length=1200)
    notice_title =  models.CharField(max_length=200)
    notice_text = models.CharField(max_length=1200)
    notice_id= models.ForeignKey(Sender_User, on_delete=models.CASCADE)
    notice_pk=models.CharField(max_length=250 ,primary_key=True , unique=True)  # notice_date + notice_id


    def __str__(self):
        return str('%s' % (self.notice_pk))




class Message_User(models.Model):


    user_phoneNumber = models.CharField(max_length=200,)
    user_name =  models.CharField(max_length=200)
    user_dong = models.CharField(max_length=50, )
    user_hosu = models.CharField(max_length=50,)
    message_User_id=models.ForeignKey(Sender_User, on_delete=models.CASCADE)
    user_pk = models.CharField(max_length=250,primary_key=True , unique=True) # user_dong +  user_hosu



    def __str__(self):
        return str('%s ' % (self.user_pk))





class Message(models.Model):
    individual_notice_text = models.CharField(max_length=1200)
    notice_url = models.CharField(max_length=600,primary_key=True , unique=True)
    notice_pk  =models.ForeignKey(Notice, on_delete=models.CASCADE)
    isConfirmbyReceiver =models.BooleanField(default=False)
    user_pk =models.ForeignKey(Message_User, on_delete=models.CASCADE)
    notice_id=models.ForeignKey(Sender_User, on_delete=models.CASCADE)
    notice_Confirm_date =models.CharField(max_length=1200, blank=False, null=False)


    def __str__(self):
        return str('%s  ' % ( self.notice_url))



class Photo(models.Model):
    notice_pk = models.ForeignKey(Notice, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)




# https://docs.djangoproject.com/ko/3.1/intro/tutorial02/
# python manage.py makemigrations sms
#  python manage.py migrate
# python manage.py createsuperuser
