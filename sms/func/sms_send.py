# -*- coding: utf-8 -*-
import requests
import json



# 010-3994-9826|유영휸
# 010-2297-4820|최현수
# 010-2821-9669|조원철
# 010-8274-5538|이충석
# 010-2670-4239|서한솔
# 010-9654-4854|이선진
# 010-4035-6735|박승민
# 010-4775-7520|김경서
class sms_send:
    def __init__(self, name, sms_receiver):
        print('생성자 호출!')

        self.name = name.replace(" ", ",")
        self.sms_receiver = sms_receiver.replace(" ",",")

    def get_sms_receiver(self):
        return self.sms_receiver

    def send(self):

        send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기

        # ================================================================== 문자 보낼 때 필수 key값
        # API key, userid, sender, receiver, msg
        # API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용
        # '010-8274-5538','010-4035-6735','010-3994-9826','010-8274-5538','010-4775-7520'

        sms_data={'key': '7xfupc9hiyalc2gko7vrggtcbl171ej4', #api key
                'userid': 'bestysg', # 알리고 사이트 아이디
                'sender': '010-3994-9826', # 발신번호
                'receiver': self.sms_receiver, # 수신번호 (,활용하여 1000명까지 추가 가능)
                'msg': ' http://18.224.16.74/sms/1/%고객명%  YSG-test 2021'
                       '\n 독수리공지 입니다. - TEST ', #문자 내용  %고객명%

                # 'msg_type' : 'msg_type', #메세지 타입 (SMS, LMS)
                 'title' : 'YSG_TEST', #메세지 제목 (장문에 적용)
                 'destination' : '010-3994-9826|01039949826,'

                                 '010-8274-5538|01082745538,'
                                

                                 '010-4035-6735|01040356735,'
                    , # %고객명% 치환용 입력
                #'rdate' : '예약날짜',
                #'rtime' : '예약시간',
                 'testmode_yn' : 'Y', #테스트모드 적용 여부 Y/N
        }
        send_response = requests.post(send_url, data=sms_data)
        print (send_response.json())
