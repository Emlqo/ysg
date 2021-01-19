# 관리 사이트에서 sms app 을 변경가능하도록 만들기¶
# 그런데, sms app 이 관리 인덱스 페이지에서 보이지 않네요. 어디에 있을까요?
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin


from .models import Message,Message_User,Notice

class MessageAdmin(ImportExportMixin, admin.ModelAdmin ):
    pass
admin.site.register(Message,MessageAdmin)
admin.site.register(Message_User,MessageAdmin)
admin.site.register(Notice,MessageAdmin)