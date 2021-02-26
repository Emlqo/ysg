from django.urls import path

from . import views
app_name ='sms'
urlpatterns = [
    path('index/', views.index, name='index'),

    path('message_User_insert/', views.message_User_insert, name='message_User_insert'),


    path('admin/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_submit/', views.register_submit, name='register_submit'),
    path('upload/', views.upload, name='upload'),
    path('createNotice/', views.createNotice, name='createNotice'),
    path('insert_notice/', views.insert_notice, name='insert_notice'),
    path('noticeDetail/<str:notice_pk>/', views.noticeDetail, name='noticeDetail'),
    path('m_noticeDetail/<str:notice_url>/', views.m_noticeDetail, name='m_noticeDetail'),


]