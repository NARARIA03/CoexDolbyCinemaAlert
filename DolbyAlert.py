# Megabox Coex Dolby Cinema Alert Coding

# 2022-08-17 Start

# 2022-09-07 Fin

# Use Python

from datetime import date, timedelta

import requests

import telegram

import json

from bs4 import BeautifulSoup


def split_movies_by_no(response):
    movie_no_list = get_movie_no_list(response)
    for movie_no in movie_no_list:
        movies = [item for item in response if item["movieNo"] == movie_no]
        title = movies[0]["movieNm"]
        timetable = get_time_table(movies)
        bot.sendMessage(chat_id=5327778681, text = title)
        # 텔레그램 봇에 영화 제목 전달
        bot.sendMessage(chat_id=5327778681, text=timetable)
        # 텔레그램 봇에 상영시간과 남은 좌석 전달
        bot.sendMessage(chat_id=5327778681, text='---------------------------')
        # 가독성을 위해서 영화 제목과 남은 좌석 전달 후 구분선 전달



def get_movie_no_list(response):
    movie_no_list = []
    for item in response:
        movie_no = item["movieNo"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list


def get_time_table(movies):
    tuples = []
    for movie in movies:
        time = movie["playStartTime"]
        seats = movie["restSeatCnt"]
        tuple = (time, seats)
        tuples.append(tuple)
    return tuples


def get_movie_no_list(response):
    movie_no_list = []
    for item in response:
        movie_no = item["movieNo"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list


url = 'https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do'
today = date.today()
# 오늘 날짜를 불러옴 (프로그램에서 자체적으로 오늘부터 크롤링하게 하기 위함)
date = today.strftime('%Y%m%d')
# 오늘 날짜를 YYMMDD형태로(매박 형태로) 수정
printdate = today.strftime('<<<%m월 %d일>>>')
# 날짜 가독성을 높히기 위해 형태 수정(이 변수는 텔레그램 메시지에 들어갈 변수다)
i = 1
# 반복문을 돌리기 위한 수

bot = telegram.Bot(token='5746775017:AAEC8aNtLTHqeE3YLuMJgcIfdYdWY_z1uzQ')
#텔레그램 봇 연동 코드


#   오늘과 내일의 상영시간표를 비교해서 같으면 크롤링 중지를 하기 위해 오늘 데이터는 반복문 밖에서 크롤링함
parameters = {"masterType": "brch",
                  "detailType": "spcl",
                  "theabKindCd": "DBC",
                  "brchNo": "1351",
                  "firstAt": "N",
                  "playDe": date,
                  #날짜를 변수로 넣어서 수정가능하게 바꿈
                  "brchNo1": "1351",
                  "spclbYn1": "Y",
                  "theabKindCd1": "DBC",
                  "crtDe": "20220817"}
                 
bot.sendMessage(chat_id=5327778681, text=printdate)
# 날짜 먼저 표시
response = requests.post(url, data=parameters).json()
# 크롤링한 데이터를 response에 넣음
movie_response = response['megaMap']['movieFormList']
# response에서 영화제목과 상영관 자리 데이터를 따로 저장
split_movies_by_no(movie_response)
# 저장한 데이터를 보기 쉽게 분리
today += timedelta(days=1)
# 내일 상영정보를 찾기위해 날짜+1
date = today.strftime('%Y%m%d')
# 날짜+1한 날짜를 yymmdd형태로 다시 수정해서 date변수에 넣음
printdate = today.strftime('<<<%m월 %d일>>>')
# 출력용 날짜도 +1일 시킴
compare_response = movie_response
# 분리해서 저장한 데이터를 비교response에 넣어서 내일과 비교


while i <= 10:
    # 반복문 (내일부터 며칠 후 상영정보까지 긁기 위함), 아래 내용은 위의 오늘 크롤링과 거의 일치
    parameters = {"masterType": "brch",
                  "detailType": "spcl",
                  "theabKindCd": "DBC",
                  "brchNo": "1351",
                  "firstAt": "N",
                  "playDe": date,  
                  "brchNo1": "1351",
                  "spclbYn1": "Y",
                  "theabKindCd1": "DBC",
                  "crtDe": "20220817"}
    response = requests.post(url, data=parameters).json()
    movie_response = response['megaMap']['movieFormList']
    #다음날짜의 movie_response까지만 출력 후 if문에 넣어서 분기

    if compare_response == movie_response:
        exit()
        #어제와 오늘 데이터가 같다면 프로그램 종료
    else:
        #어제와 오늘 데이터가 다르다면 크롤링 후 텔레그램으로 전송
        parameters = {"masterType": "brch",
                  "detailType": "spcl",
                  "theabKindCd": "DBC",
                  "brchNo": "1351",
                  "firstAt": "N",
                  "playDe": date,
                  "brchNo1": "1351",
                  "spclbYn1": "Y",
                  "theabKindCd1": "DBC",
                  "crtDe": "20220817"}

        bot.sendMessage(chat_id=5327778681, text=printdate)
        response = requests.post(url, data=parameters).json()
        movie_response = response['megaMap']['movieFormList']
        split_movies_by_no(movie_response)
        today += timedelta(days=1)
        date = today.strftime('%Y%m%d')
        printdate = today.strftime('<<<%m월 %d일>>>')
        i += 1
        compare_response = movie_response
        #내일과 내일모래 비교를 위한 변수 조정