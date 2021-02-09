# 관리 사이트에서 sms app 을 변경가능하도록 만들기¶
# 그런데, sms app 이 관리 인덱스 페이지에서 보이지 않네요. 어디에 있을까요?
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export import resources
from import_export.admin import  ImportExportActionModelAdmin


from .models import Message, Message_User, Notice, Sender_User, Photo


class Message_UserResource(resources.ModelResource):
    class Meta:
        model = Message_User
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('user_phoneNumber',)



class MessageAdmin(ImportExportActionModelAdmin):
    pass
admin.site.register(Message,MessageAdmin)
admin.site.register(Message_User,MessageAdmin)

admin.site.register(Sender_User,MessageAdmin)

# Photo 클래스를 inline으로 나타낸다.
class PhotoInline(admin.TabularInline):
    model = Photo

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다.
class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

# Register your models here.
admin.site.register(Notice, PostAdmin)