from django.urls import path

from . import views
app_name ='sms'
urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('message_User_insert/', views.message_User_insert, name='message_User_insert'),
    path('<str:notice_key>/<str:notice_url>', views.notice_view, name='url'),
    path('<str:notice_key>/', views.admin, name='admin'),

]