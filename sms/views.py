from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
import sqlite3
import datetime

import openpyxl, pyexcel
from .models import Message, Message_User, Notice, Photo, Sender_User
import pandas as pd
from django.template import loader

from .func.katalk_send import katalk_send
# Create your views here.
from urllib import parse
from openpyxl import load_workbook
from .forms import UploadFileForm

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest


#-------------------함수 기반 view---------------------
# render 안쓴 것
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('sms/index_test.html')
#     context = {
#         'latest_question_list': latest_question_list,  # context를 통해 데이터를 전달
#     }
#     return HttpResponse(template.render(context, request))
# render 적용



def index(request):
    if request.method == 'GET':
        conn = sqlite3.connect('./db.sqlite3')
        cur = conn.cursor()
        user_id = request.session.get('user')
        print(user_id)


        sql = "select * from sms_notice where notice_id_id =?"
        cur.execute(sql, [user_id])
        rows = cur.fetchall()
        rows = pd.DataFrame(rows)

        rows.rename(columns={0:"date", 1:"title",2:"text"},inplace=True)
        print(rows)
        date =[]
        for i in rows['date']:
            date.append(i[:16])


        title = rows['title']
        text = rows['text']

        history_data= zip(date,title,text)

        request.session['user'] = request.POST.get('id')
        ## 공지 보낸 페이지 여기 까지


        ##=========== 유저 목록 데이터 ============

        sql = "select * from sms_Message_User where message_User_id_id =?"
        cur.execute(sql, [user_id])
        rows = cur.fetchall()
        rows = pd.DataFrame(rows)
        print(rows)
        rows.rename(columns={0: "user_phoneNumber", 1: "user_name", 2: "user_dong",3:"user_hosu"}, inplace=True)
        print(rows)


        user_phoneNumber = rows['user_phoneNumber']
        user_name = rows['user_name']
        user_dong = rows['user_dong']
        user_hosu = rows['user_hosu']

        sql = "select distinct user_dong from sms_Message_User where message_User_id_id =?"
        cur.execute(sql, [user_id])

        rows = cur.fetchall()
        group_list = []
        for i in range(len(rows)):
            group_list.append(rows[i][0])



        user_data = zip(user_phoneNumber, user_name, user_dong,user_hosu)


        print("?")
        print(group_list)

        return render(request, 'sms/index.html',{"history_data":history_data, "user_data":user_data,"group":group_list})
    # conn = sqlite3.connect('./db.sqlite3')
    # cur = conn.cursor()
    # sql = "select distinct user_dong from  main.sms_message_user"
    #
    # cur.execute(sql)
    # rows = cur.fetchall()
    #
    # group_list=[]
    # for i in range(len(rows)):
    #     group_list.append(rows[i][0])
    #
    #
    #
    # return render(request, 'sms/index_test.html',{'kind': group_list})

def createNotice(request):

    if request.method == 'GET':
        conn = sqlite3.connect('./db.sqlite3')
        cur = conn.cursor()
        user_id = request.session.get('user')



        sql = "select distinct user_dong from sms_Message_User where message_User_id_id =?"
        cur.execute(sql, [user_id])

        rows = cur.fetchall()
        group_list = []
        for i in range(len(rows)):
            group_list.append(rows[i][0])


        return render(request,'sms/createNotice.html')
    if request.method == 'POST':
        # phone_number = request.POST.getlist('phone_number')
        # name = request.POST.getlist('name')

        conn = sqlite3.connect('./db.sqlite3')
        cur = conn.cursor()

        # 공지 DB Insert

        notice_text = request.POST.get('notice_text')
        notice_title = request.POST.get('notice_title')
        user_id = request.session.get('user')

        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

        # sender_User = Sender_User()
        # notice = Notice()
        # notice.notice_id = sender_User
        # notice.notice_date = nowDatetime
        # notice.notice_title = request.POST.get('notice_title')
        # notice.notice_text = request.POST.get('notice_text')
        # notice.notice_id = request.POST.get('notice_id')
        # notice.notice_ps = request.POST.get('notice_ps')
        # notice.save()

        sql = "insert into sms_notice (notice_date,notice_title,notice_text,notice_id_id) values (?,?,?,?)"

        cur.execute(sql, [nowDatetime, str(notice_title), str(notice_text), str(user_id), ])

        conn.commit()

        phone_number = request.POST.get('phone_number')
        if phone_number == '':

            # 알림톡 수신자 data 가져오기
            group = request.POST.get('group')
            if group == '전체':
                sql = "select * from  main.sms_message_user"
                cur.execute(sql)
            else:
                sql = "select * from  main.sms_message_user where user_group = ? "

                cur.execute(sql, [group])

            rows = cur.fetchall()

            rows = pd.DataFrame(rows)

            phone_number_list = rows[0]
            name = rows[1]

        else:
            phone_number_list = []
            phone_number_list.append(phone_number)
            sql = "select * from  main.sms_message_user where user_phoneNumber = ? "

            cur.execute(sql, [phone_number])
            rows = cur.fetchall()

            rows = pd.DataFrame(rows)
            name = rows[1]

        for img in request.FILES.getlist('imgs'):
            # Photo 객체를 하나 생성한다.
            # photo = Photo()
            # # 외래키로 현재 생성한 Notice의 기본키를 참조한다.
            # photo.notice_date = notice
            # # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            # photo.image = img
            # # 데이터베이스에 저장
            # photo.save()

            sql = "insert into sms_photo (notice_date_id,image) values (?,?)"

            cur.execute(sql, [nowDatetime, str(img)])

            conn.commit()

        cur.close()
        conn.close()

        # limit_time = request.POST.get('limit_time')
        send = katalk_send(name, phone_number_list, str(notice_text), str(notice_title), str("12시"), str(notice_id),
                           str(nowDatetime))
        send.send()

    return HttpResponseRedirect(
        reverse('sms:index', ))


def register(request):

    return render(request, 'sms/register.html')

def register_submit(request):
    try:

        if request.method == 'POST':

            conn = sqlite3.connect('./db.sqlite3')
            cur = conn.cursor()
            sql = "select * from sms_Sender_User where id =?"
            cur.execute(sql,[str(request.POST.get('id'))] )
            rows = cur.fetchall()

            if len(rows)>0:

                return HttpResponse("ID가 중복 되거나 기타 오류 입니다.")



            sender_User = Sender_User()
            sender_User.id=request.POST.get('id')
            sender_User.ps =request.POST.get('ps')
            sender_User.aptNm =request.POST.get('aptNm')
            sender_User.complexNm =request.POST.get('complexNm')
            sender_User.villageNm =request.POST.get('villageNm')
            sender_User.aptAddress =request.POST.get('aptAddress')
            sender_User.save()

            return redirect('/sms/login/')
    except:
        return HttpResponse("ID가 중복 되거나 기타 오류 입니다.")

def upload(request):

    if request.method == "POST":
        user_id = request.session.get('user')


        form = UploadFileForm(request.POST, request.FILES)


        if form.is_valid():

            conn = sqlite3.connect('./db.sqlite3')
            cur = conn.cursor()

            excel_file = request.FILES["file"]
            wb = openpyxl.load_workbook(excel_file)
            # getting a particular sheet by name out of many sheets


            excel_data = list()
            # iterating over the rows and
            # getting value from each cell in row
            ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
            for row in ws.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))

                   # print(str(cell.value), "row_data")
                row_data.append(user_id)
                excel_data.append(row_data)
            del excel_data[0]
            for data in excel_data:

                sql = "insert into sms_Message_User (user_phoneNumber,user_name,user_dong,user_hosu,message_User_id_id) values (?,?,?,?,?)"

                cur.execute(sql, data)

                conn.commit()


                # message_User = Message_User()
                # message_User.user_phoneNumber =
                # message_User.user_name =
                # message_User.user_dong =
                # message_User.user_hosu =
                # message_User.message_User_id =
                # message_User.save()




            # excel_data = list()
            # # iterating over the rows and
            # # getting value from each cell in row
            # for row in worksheet.iter_rows():
            #     row_data = list()
            #     for cell in row:
            #         row_data.append(str(cell.value))
            #     excel_data.append(row_data)
            #
            #
            #
            # request.FILES['file'].save_to_database(
            #     model=Message_User,
            #     mapdict=['user_phoneNumber', 'user_name', 'user_dong','user_hosu','message_User_id'])
            request.session['user'] = request.POST.get('id')
            return render(request, 'sms/index_test.html')
        else:

            return HttpResponseBadRequest(form.is_valid())
    else:
        return render(request, 'sms/index_test.html')




def login(request):
    if request.method == 'GET':
        return render(request, 'sms/login.html')

    if request.method == 'POST':
        print("POST")
        # phone_number = request.POST.getlist('phone_number')
        # name = request.POST.getlist('name')

        conn = sqlite3.connect('./db.sqlite3')
        cur = conn.cursor()

        # 공지 DB Insert

        # id = request.POST.get('id')
        # ps = request.POST.get('ps')

        sql = "select * from sms_Sender_User where id =? and ps =?"
        cur.execute(sql, [str(request.POST.get('id')), str(request.POST.get('ps'))])
        rows = cur.fetchall()
        if len(rows) == 1:
            request.session['user'] = request.POST.get('id')
            return redirect('/sms/index/')
        else:
            return HttpResponse("ID가 중복 되거나 없는 ID 입니다.")



    #return render(request, 'sms/login_test.html') ## form


def message_User_insert(request):

    if request.method == "POST":

        form = UploadFileForm(request.POST, request.FILES)


        if form.is_valid():

            request.FILES['file'].save_to_database(
                model=Message_User,
                mapdict=['user_phoneNumber', 'user_name', 'user_group'])
            return HttpResponse("OK")
        else:

            return HttpResponseBadRequest(form.is_valid())
    else:
        return render(request, 'sms/index_test.html')






def submit(request):

    if request.method =='POST':
        # phone_number = request.POST.getlist('phone_number')
        # name = request.POST.getlist('name')

        conn = sqlite3.connect('./db.sqlite3')
        cur = conn.cursor()

        # 공지 DB Insert

        notice_text = request.POST.get('notice_text')
        notice_title = request.POST.get('notice_title')
        notice_id = request.POST.get('notice_id')
        notice_ps = request.POST.get('notice_ps')

        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')


        # sender_User = Sender_User()
        # notice = Notice()
        # notice.notice_id = sender_User
        # notice.notice_date = nowDatetime
        # notice.notice_title = request.POST.get('notice_title')
        # notice.notice_text = request.POST.get('notice_text')
        # notice.notice_id = request.POST.get('notice_id')
        # notice.notice_ps = request.POST.get('notice_ps')
        # notice.save()


        sql = "insert into sms_notice (notice_date,notice_title,notice_text,notice_id_id,notice_ps) values (?,?,?,?,?)"

        cur.execute(sql, [nowDatetime, str(notice_title),  str(notice_text),str(notice_id),str(notice_ps)])

        conn.commit()


        phone_number = request.POST.get('phone_number')
        if phone_number=='':

            # 알림톡 수신자 data 가져오기
            group = request.POST.get('group')
            if group == '전체':
                sql = "select * from  main.sms_message_user"
                cur.execute(sql)
            else:
                sql = "select * from  main.sms_message_user where user_group = ? "

                cur.execute(sql,[group])

            rows = cur.fetchall()

            rows = pd.DataFrame(rows)

            phone_number_list = rows[0]
            name = rows[1]

        else:
            phone_number_list =[]
            phone_number_list.append(phone_number )
            sql = "select * from  main.sms_message_user where user_phoneNumber = ? "

            cur.execute(sql, [phone_number])
            rows = cur.fetchall()

            rows = pd.DataFrame(rows)
            name = rows[1]




        for img in request.FILES.getlist('imgs'):
            # Photo 객체를 하나 생성한다.
            # photo = Photo()
            # # 외래키로 현재 생성한 Notice의 기본키를 참조한다.
            # photo.notice_date = notice
            # # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            # photo.image = img
            # # 데이터베이스에 저장
            # photo.save()

            sql = "insert into sms_photo (notice_date_id,image) values (?,?)"

            cur.execute(sql, [nowDatetime,str(img)])

            conn.commit()




        cur.close()
        conn.close()


        # limit_time = request.POST.get('limit_time')
        send = katalk_send(name, phone_number_list , str( notice_text) , str( notice_title) , str( "12시") , str(notice_id) ,str(nowDatetime) )
        send.send()



    return HttpResponseRedirect(
             reverse('sms:index', ))



def notice_view(request,notice_id ,notice_url):
    if request.method == 'GET':
        print(notice_url)



        conn = sqlite3.connect('./db.sqlite3')
        cur = conn.cursor()
        # print(parse.quote(notice_url))
        # notice_url =  str(parse.quote(notice_url).lower())
        sql = "select  user_phoneNumber_id from main.sms_message WHERE notice_url  = ?"
       # print(notice_url)  ## 2021-01-27 16:17:5001082745538      날짜 pk 랑 휴대전화 나눠야함
        cur.execute(sql,[notice_url])
        rows = cur.fetchall()



        #
        # STATIC_ROOT = BASE_DIR.joinpath('static')
        # STATIC_URL = '/static/'
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

        cur.execute("UPDATE main.sms_message SET isConfirmbyReceiver = True , notice_Confirm_date = ? WHERE user_phoneNumber_id = ? ",[nowDatetime,rows[0][0]])


        message_User =  get_object_or_404(Message_User,pk=rows[0][0])

        message = get_object_or_404(Message,pk=notice_url)

        notice = get_object_or_404(Notice, pk=notice_url[:19])
        sql = "select  image from main.sms_Photo WHERE notice_date_id  = ?"
        # print(notice_url)  ## 2021-01-27 16:17:5001082745538      날짜 pk 랑 휴대전화 나눠야함
        cur.execute(sql, [notice_url[:19]])
        rows = cur.fetchall()
        print(rows)
        photo =  rows[0][0]
        conn.commit()
        cur.close()
        conn.close()

        #return  redirect('https://www.naver.com/')  ## 절대 경로 가능 => 기업 내

        return render(request,'sms/nt_view.html',{'message' : message, 'notice' : notice , 'message_User' : message_User,'photo':photo} )


def admin(request, notice_id):
        conn = sqlite3.connect('./db.sqlite3')
        cur = conn.cursor()
        # print(parse.quote(notice_url))
        # notice_url =  str(parse.quote(notice_url).lower())
        name_list = []
        sql = "select * from  sms_message where notice_id_id  = ?"

        cur.execute(sql, [notice_id])
        rows = cur.fetchall()
        for name in rows:

            sql = "select user_name from  sms_Message_User where user_phoneNumber = ?"

            cur.execute(sql, [name[5]])
            name_list.append(cur.fetchall()[0])



        conn.commit()
        cur.close()
        conn.close()
        rows =pd.DataFrame(rows)
        rows['name']=name_list

        rows.rename(columns={0:"notice_text", 1:"날짜 + 번호 URL",2:"isConfirmbyReceiver",3:"날짜"}, inplace=True)

        del rows[4]
        del rows[5]
        result = rows.to_html()

        return render(request, 'sms/admin_nt_view.html', {'result': result})
