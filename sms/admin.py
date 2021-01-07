# 관리 사이트에서 sms app 을 변경가능하도록 만들기¶
# 그런데, sms app 이 관리 인덱스 페이지에서 보이지 않네요. 어디에 있을까요?
from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Message,User

admin.site.register(Message)
admin.site.register(User)
