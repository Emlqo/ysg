from django.urls import path

from . import views
app_name ='sms'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('message_User_insert/', views.message_User_insert, name='message_User_insert'),
    path('<str:notice_id>/<str:notice_url>', views.notice_view, name='url'),

    path('admin/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_submit/', views.register_submit, name='register_submit'),
    path('upload/', views.upload, name='upload'),
    path('createNotice/', views.createNotice, name='createNotice'),


]