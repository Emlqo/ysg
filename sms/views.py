from django import forms
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
import sqlite3
import datetime

import openpyxl, pyexcel
from .models import Message, Message_User,Notice
import pandas as pd
from django.template import loader
from django.shortcuts import render
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
#     template = loader.get_template('sms/index.html')
#     context = {
#         'latest_question_list': latest_question_list,  # context를 통해 데이터를 전달
#     }
#     return HttpResponse(template.render(context, request))

# render 적용
def index(request):
    conn = sqlite3.connect('./db.sqlite3')
    cur = conn.cursor()
    sql = "select distinct user_group from  main.sms_message_user"

    cur.execute(sql)
    rows = cur.fetchall()

    group_list=[]
    for i in range(len(rows)):
        group_list.append(rows[i][0])



    return render(request, 'sms/index.html',{'kind': group_list})



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
        return render(request, 'sms/index.html')






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
        print(nowDatetime , notice_title, notice_text,notice_id ,notice_ps)


        sql = "insert into sms_notice (notice_date,notice_title,notice_text,notice_id_id,notice_ps) values (?,?,?,?,?)"

        cur.execute(sql, [nowDatetime, str(notice_title),  str(notice_text),str(notice_id),str(notice_ps)])

        conn.commit()




        # 알림톡 수신자 data 가져오기
        group = request.POST.get('group')
        if group == '전체':
            sql = "select * from  main.sms_message_user"
            cur.execute(sql)
        else:
            sql = "select * from  main.sms_message_user where user_group = ? "
            cur.execute(sql, group)

        rows = cur.fetchall()

        rows = pd.DataFrame(rows)

        phone_number = rows[0]
        name = rows[1]



        cur.close()
        conn.close()


        # limit_time = request.POST.get('limit_time')
        send = katalk_send(name, phone_number , str( notice_text) , str( notice_title) , str( "12시") , str(notice_id) ,str(nowDatetime) )
        send.send()



    return HttpResponseRedirect(
             reverse('sms:index', ))


def notice_view(request,notice_id ,notice_url):
    conn = sqlite3.connect('./db.sqlite3')
    cur = conn.cursor()
    # print(parse.quote(notice_url))
    # notice_url =  str(parse.quote(notice_url).lower())
    sql = "select  user_phoneNumber_id from main.sms_message WHERE notice_url  = ?"
    print(notice_url)  ## 2021-01-27 16:17:5001082745538      날짜 pk 랑 휴대전화 나눠야함
    cur.execute(sql,[notice_url])
    rows = cur.fetchall()
    print(rows)
    print(notice_url[:19])
    print(rows[0][0])

    cur.execute("UPDATE main.sms_message SET isConfirmbyReceiver = True WHERE user_phoneNumber_id = ? ",[rows[0][0]])
    conn.commit()
    cur.close()
    conn.close()

    message_User =  get_object_or_404(Message_User,pk=rows[0][0])
    print("1")
    message = get_object_or_404(Message,pk=notice_url)
    print("2")
    notice = get_object_or_404(Notice, pk=notice_url[:19])
    print("3")

    return render(request,'sms/nt_view.html',{'message' : message, 'notice' : notice , 'message_User' : message_User} )

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
            print(name[5])
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

    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])  # https://milhouse93.ti
    #     # story.com/69  choice_set 설명 선택지에서 고른 초이스id를 가져옴 밑에 확인 name이 choice라 []안에 choice로 들어가는것
    #     # <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    #     # 순서대로 보면 처음에 question 객체를 가져옴 어떻게? 이미 detail.html은 question 객체 하나로 이루어져있음 그안에 선택지 사항들이 있는것
    #     # 거기서 투표를 라디오 버튼으로 하나만 골라서 진행이됨 그럼 어떤것을 눌렀는지 확인을 해야함
    #     # 확인 하는 방법이 일단 question 객체를 불러옴  그리고 그 question 객체에 지금 사용자가 누른 choice를 불러와야함
    #     # 그 작업이 post choice로 누른 id값을 가져옴
    #     # 가져온후 그 choice 모델에 투표 되었다고 +1 해주고 저장함
    #     # 요약 question 객체에서 사용자가 입력한 id를 이용해 choice를 가져온후 +1 해주고 저장함
    # except (KeyError, Choice.DoesNotExist):  # 만약 POST자료에 choice가 없으면 에러 발생  에러 발생하면 에러 메시지와 함께 다시 detail 페이지로 이동
    #     # Redisplay the question voting form.
    #     return render(request, 'sms/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1  ## 지금 골라진 choice에 투표수를 하나 증가시킨후 저장한다 실제 관리자 페이지 가서 확인해보면 증가되어있음 ㅇㅇ
    #     ##. votes 의 조회값이 42라고 할 경우, 두 명의 사용자에게 새로운 값인 43이 계산 되고, 저장됩니다. 그러나 44가 되야되겠죠.
    #     ##이를 경쟁 상태 라 합니다. 이 문제를 해결할 수 있는 방법을 알아보려면 Avoiding race conditions using F() 를 참고하세요.
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     # https://wayhome25.github.io/django/2017/05/05/django-url-reverse/ reverse 정리
    #     return HttpResponseRedirect(
    #         reverse('sms:results', args=(question.id,)))  ## reverse를 사용하여 하드 코딩이 아님 ex /sms/3/results  여기서




# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)  v1

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")   ## 404 예외처리 기능 , raise 예외 발생시키기 (메시지) v2
#     return render(request,'sms/detail.html',{'question':question})

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)   ##  try catch 문 생략 가능 get_object_or_404
#     return render(request, 'sms/detail.html', {'question': question})  # v3
#get_object_or_404() 함수는 Django 모델을 첫번째 인자로 받고,
# 몇개의 키워드 인수를 모델 관리자의 get() 함수에 넘깁니다.
# 만약 객체가 존재하지 않을 경우, Http404 예외가 발생합니다.

# def results(request, question_id):
#     question = get_object_or_404(Question,pk=question_id)
#
#     return render(request,'sms/nt_view.html',{'question' : question})
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)  ## question 객체를 불러온다 그중 프라이머리키(기본키)가 question_id 인것으로
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])  # https://milhouse93.ti
#         # story.com/69  choice_set 설명 선택지에서 고른 초이스id를 가져옴 밑에 확인 name이 choice라 []안에 choice로 들어가는것
#         # <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
#         # 순서대로 보면 처음에 question 객체를 가져옴 어떻게? 이미 detail.html은 question 객체 하나로 이루어져있음 그안에 선택지 사항들이 있는것
#         # 거기서 투표를 라디오 버튼으로 하나만 골라서 진행이됨 그럼 어떤것을 눌렀는지 확인을 해야함
#         # 확인 하는 방법이 일단 question 객체를 불러옴  그리고 그 question 객체에 지금 사용자가 누른 choice를 불러와야함
#         # 그 작업이 post choice로 누른 id값을 가져옴
#         # 가져온후 그 choice 모델에 투표 되었다고 +1 해주고 저장함
#
#         # 요약 question 객체에서 사용자가 입력한 id를 이용해 choice를 가져온후 +1 해주고 저장함
#
#     except (KeyError, Choice.DoesNotExist):  # 만약 POST자료에 choice가 없으면 에러 발생  에러 발생하면 에러 메시지와 함께 다시 detail 페이지로 이동
#         # Redisplay the question voting form.
#         return render(request, 'sms/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1  ## 지금 골라진 choice에 투표수를 하나 증가시킨후 저장한다 실제 관리자 페이지 가서 확인해보면 증가되어있음 ㅇㅇ
#
#         ##. votes 의 조회값이 42라고 할 경우, 두 명의 사용자에게 새로운 값인 43이 계산 되고, 저장됩니다. 그러나 44가 되야되겠죠.
#         ##이를 경쟁 상태 라 합니다. 이 문제를 해결할 수 있는 방법을 알아보려면 Avoiding race conditions using F() 를 참고하세요.
#
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         # https://wayhome25.github.io/django/2017/05/05/django-url-reverse/ reverse 정리
#         return HttpResponseRedirect(reverse('sms:results', args=(question.id,))) ## reverse를 사용하여 하드 코딩이 아님 ex /sms/3/results  여기서 3은 question.id 임
## HttpResponseRedirect 현재 APP에서 다른 APP으로 이동해주는 url Redirect를 해준다
##==> render를 써서 다른 html 로 보내는게 아니라 아예 app내에 urls.py 로 보낸다음 거기에 results로 보내는거 인자는 question.id

## view에서는 request 라는 인자를 받고  HttpResponse 로 리턴함
## 클라이언트에서 request를 받으면 여러가지 정보가 들어있음


## GET 과 POST 차이
# GET은 주소줄에 값이 ?뒤에 쌍으로 이어붙고 POST는 숨겨져서(body안에) 보내진다.
# GET은 URL에 이어붙기 때문에 길이제한이 있어서 많은양의 데이터는 보내기 어렵고 POST는 많은 양의 보내기에도 적합하다.(역시 용량제한은 있지만)
#  https://hongsii.github.io/2017/08/02/what-is-the-difference-get-and-post/
# 즉 http://url/bbslist.html?id=5&pagenum=2 같이 하는 것이 GET방식이고 form을 이용해서 submit을 하는 형태가 POST입니다. 물론 form submit get도 됨 하지만 길이 제약 때문에 거의 안씀
# get은  말그대로 가져오는것 select     post는 수행하는 느낌 create
# https://velog.io/@magnoliarfsit/ReDjango-3.-GET-POST-%EB%A9%94%EC%86%8C%EB%93%9C-%EC%B0%A8%EC%9D%B4%EC%A0%90-%EB%B0%8F-api-%EC%84%A4%EA%B3%84


#------------------------클래스스 기반 view--------------------
#
# class IndexView(generic.ListView):
#     template_name = 'sms/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'sms/detail.html'
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'sms/nt_view.html'
#
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'sms/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('sms:results', args=(question.id,)))