# -*- coding: utf-8 -*-
import sqlite3

import requests
import json


#
# 템플릿 신청하실 때 웹링크버튼 url을 http://#{링크1} 또는 https://#{링크2} 와 같이 변수처리하셨다면
# 발송시마다 링크 변경가능합니다.
# 다만, 변수처리하지 않고 고정값으로 입력하여 템플릿 신청하셨다면 신청하신 url그대로 사용해주셔야 합니다ㅣ.
#  send = katalk_send(str(name), str( phone_number) , str( notice_text) , str( notice_title) , str( limit_time)  )
class katalk_send:
    def __init__(self, name, sms_receiver , user_dong_hosu_list, notice_text  ,notice_title ,limit_time, notice_id , nowDatetime):


        self.name = name
        self.sms_receiver = sms_receiver
        self.user_dong_hosu_list = user_dong_hosu_list

        self.sms_receiver_len = len(sms_receiver)
        self.notice_text = notice_text
        self.notice_title = notice_title
        self.limit_time = limit_time
        self.notice_id = notice_id
        self.nowDatetime = nowDatetime







    def get_sms_receiver(self):
        return self.sms_receiver

    def send(self):
        conn = sqlite3.connect('./db.sqlite3')
        cur = conn.cursor()


        basic_send_url = 'https://kakaoapi.aligo.in/akv10/alimtalk/send/'  # 요청을 던지는 URL, 알림톡 전송
        button_info = []
        for i in range(self.sms_receiver_len):

            button_info.append( {'button': [{'name': '공지 확인',  # 버튼명
                                       'linkType': 'WL',  # DS, WL, AL, BK, MD
                                       'linkTypeName': '웹링크',  # 배송조회, 웹링크, 앱링크, 봇키워드, 메시지전달 중에서 1개
                                       'linkM': 'http://13.58.164.35:8000/' +self.nowDatetime+ str(self.user_dong_hosu_list[i]+self.notice_id),  # WL일 때 필수
                                       'linkP': 'http://13.58.164.35:8000/'+self.nowDatetime+str(self.user_dong_hosu_list[i]+self.notice_id),  # WL일 때 필수
                                       # 'linkI': 'IOS app link', # AL일 때 필수
                                       # 'linkA': 'Android app link' # AL일 때 필수
                                       }]})

        ''' 만약 button이 여러개이면, 'button'key의 value list에 버튼 개수만큼 dict를 추가해주시면 됩니다.
        button_info = {'button': [{'name':'1번버튼', ~}, {'name':'2번버튼', ~}, {'name':~}]} '''

        # button_info = {'button': [{'name': '공지 확인',  # 버튼명
        #                            'linkType': 'WL',  # DS, WL, AL, BK, MD
        #                            'linkTypeName': '웹링크',  # 배송조회, 웹링크, 앱링크, 봇키워드, 메시지전달 중에서 1개
        #                            'linkM': 'http://3.140.216.53:8000/01082745538',  # WL일 때 필수
        #                            'linkP': 'http://3.140.216.53:8000/01082745538',  # WL일 때 필수
        #                            # 'linkI': 'IOS app link', # AL일 때 필수
        #                            # 'linkA': 'Android app link' # AL일 때 필수
        #                            }]}


        basic_send_url1 = 'https://kakaoapi.aligo.in/akv10/token/create/30/s/'  # 요청을 던지는 URL, 현재는 토큰생성

        sms_data1 = {'apikey': '7xfupc9hiyalc2gko7vrggtcbl171ej4',  # api key
                     'userid': 'bestysg',  # 알리고 사이트 아이디
                     }

        create_token_response = requests.post(basic_send_url1, data=sms_data1)

        # button_info = json.dumps(button_info) # button의 타입은 JSON 이어야 합니다.

        sms_data = {'apikey': '7xfupc9hiyalc2gko7vrggtcbl171ej4',  # api key
                    'userid': 'bestysg',  # 알리고 사이트 아이디
                    'token': create_token_response.json()['token'],  # 생성한 토큰
                    'senderkey': '0677997695e39d55cdac33f71b8d8cd7294c9098',
                    'tpl_code': 'TD_6755',  # 템플릿 코드
                    'sender': '01039949826',  # 발신자 연락처,
                    # 'senddate': '19000131120130', # YYYYMMDDHHmmss
         #            'receiver_1' : '01082745538',
         # 'message_1': '독수리공지에서 공지가 도착 했습니다!!이충석님 dddd을 7시 까지 열람 가능합니다.',
         #            'button_1': json.dumps(button_info),
                    'subject_1': 'Title',  # 알림톡 제목 - 수신자에게는 표기X
                    # 'failover': 'Y or N', # 실패시 대체문자 전송 여부(템플릿 신청시 대체문자 발송으로 설정하였더라도 Y로 입력해야합니다.)
                    # 'fsubject_1': '대체문자 제목', # 실패시 대체문자 제목
                    # 'fmessage_1': '대체문자 내용', # 실패시 대체문자 내용
                    'testMode': 'N',  # 테스트 모드 적용여부(기본N), 실제 발송 X
                    }


        for i in range(self.sms_receiver_len):
            sms_data['receiver_'+str(i+1)]=self.sms_receiver[i]
            sms_data['message_'+str(i+1)] ="오손도손 에서 공지가 도착 했습니다!!\n"\
                                           +self.name[i]+'님\n'+self.notice_title+'을\n'+self.limit_time+' 까지 열람 가능합니다.'
            sms_data['button_'+str(i+1)] =json.dumps(button_info[i])
            sql = "insert into sms_Message ( individual_notice_text,notice_url  , notice_pk_id, isConfirmbyReceiver ,user_pk_id ,notice_id_id,notice_Confirm_date)values (?,?,?,?,?,?,?)"



            cur.execute(sql, [self.notice_text,self.nowDatetime + str(self.user_dong_hosu_list[i] + self.notice_id) ,
                              str(self.nowDatetime+ self.notice_id), False, str(self.sms_receiver[i]+ self.notice_id), str(self.notice_id),str(self.nowDatetime)])

            conn.commit()


        #print(sms_data)

        alimtalk_send_response = requests.post(basic_send_url, data=sms_data)

        print(alimtalk_send_response.json())


