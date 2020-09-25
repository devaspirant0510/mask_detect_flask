
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as font
from datetime import datetime

#####################################
# 웹크롤링
url='http://ncov.mohw.go.kr/' #사이트 주소
html=urllib.request.urlopen(url).read() #주소 읽기
soup=BeautifulSoup(html,'html.parser') # html부분만 가져오기
#일일 확진자 정보 
today=soup.find_all('span',{'class':'data'}) 
cov_today=[]
for to in today:
    cov_today.append(to.get_text())
local_cov=cov_today[0]#국내확진자
global_cov=cov_today[1]#해외확진자

#누적 확진자 정보
cov_accumulate=soup.find_all('span',{'class':'num'})
cov_accumulate_now=soup.find_all('span',{'class':'before'})

cov_accumulate_li=[]#누적
for i in cov_accumulate:
    cov_accumulate_li.append(i.get_text())
cov_accumulate=cov_accumulate_li[:4]

cov_accumulate_now_li=[]#전일대비
for i in cov_accumulate_now:
    cov_accumulate_now_li.append(i.get_text())
cov_accumulate_now=cov_accumulate_now_li[:4]
#검사현황
cov_check=soup.find_all('span',{"class","num"})

check_data_li=[]
for i in cov_check:
    check_data_li.append(i.get_text())
check_data_li=check_data_li[4:7]

#시도별 확진자
citystar=soup.find_all('span',{"class":'name'})#지역이름
citynujuk=soup.find_all('button',{"type":'button'})#지역별 누적 확진자
cov_data=soup.find_all("span",{"class","num"})#지역별 확진자 데이터
cov_junill=soup.find_all("span",{"class","sub_num red"})#시도별 전일대비 확진자
citynujuk=citynujuk[3:]#필요한 부분만  슬라이싱
citylist=[]
for i in citystar:
    citylist.append(i.get_text())#리스트에 지역별 확진자 정보를 저장

dataset=[]
for i in cov_data:
    dataset.append(i.get_text())


junilldataset=[]
for i in cov_junill:
    junilldataset.append(i.get_text())

junilldataset=junilldataset[1:]#전일대비 확진자 데이터
deaddataset=dataset[33::5]#사망자 데이터
quarantine_release_dataset=dataset[32::5]# 격리해제 데이터
nujukdataset=dataset[7:25]#누적확진자 데이터
isolationdataset=dataset[31::5]#격리 데이터
####################################
