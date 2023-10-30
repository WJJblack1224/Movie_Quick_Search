'''
爬取開眼電影網的網站資料，快速查詢電影場次時間
加入PyQt5介面
'''
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from PyQt5 import QtWidgets
import sys

def _show():
    global moviePost
    movieGet = box1.currentText()
    moviePost = (movieDict[movieGet])
   

def _search():
    global moviePost
    listwidget.clear()
    areaGet = box2.currentText()
    areaPost = (areaDict[areaGet])
    search_movie = moviePost[0]
    search_area = areaPost[0]
    movie_url = "http://www.atmovies.com.tw/showtime/"+search_movie+r"/"+search_area+r"/"    
    movie_rq = requests.get(movie_url)   
    movie_rq.encoding = "utf-8"
    film_soup = BeautifulSoup(movie_rq.text,"lxml")
    film_soups = film_soup.find("div",{'id':'filmShowtimeBlock'})
    theaTers = []
    theaTers_movieTime = []

    for mysoup in film_soups.find_all("ul"):     
        listwidget.addItems([mysoup.find("li").text])   #列出戲院名稱
        theater = mysoup.find("li").text
        theaTers.append(theater)
        
        for mysoups in mysoup.find_all('li')[1:]:  
            listwidget.addItems([mysoups.text])  #列出場次時間
            listwidget.addItems(['-'*20])
            movieTime = mysoups.text
            theaTers.append(movieTime)           #將戲院名與場次時間組合成串列
        theaTers_movieTime.append(theaTers)      #各戲院與場次時間組合成二維串列
        theaTers = []
            
    dF = pd.DataFrame(theaTers_movieTime).T        #將二維串列轉成DataFrame
    dF.columns = dF.iloc[0]                        #將戲院名設為column
    dF = dF[1:]
    dF.to_csv("./MovieTime.csv",encoding='utf-8-sig')
    
moviePost = []   #預設的全域變數

#爬取本期首輪電影的名稱與對應的ID，存成字典  
url = "http://www.atmovies.com.tw/movie/now/"
rq = requests.get(url)
rq.encoding = "utf-8"
soup = BeautifulSoup(rq.text,"lxml")
soups = soup.find("ul",'filmListPA')
movie = []
film_id = []

for mysoup in soups.find_all("li"):
    movie.append(mysoup.find("a").text)
    filmtext = mysoup.find("a")["href"]
    matchWord = re.findall(r"[a-z]+\d{4,}",filmtext)
    film_id.append(matchWord)

movieList = list(zip(movie,film_id))
movieDict = dict(movieList)

#爬取地區的對應ID，存成字典  
area_url = "http://www.atmovies.com.tw/showtime/"
area_rq = requests.get(area_url)
area_rq.encoding = "utf-8"
ar_soup = BeautifulSoup(area_rq.text,"lxml")
area = []
areaID = []
ar_soups = ar_soup.find("ul",'theaterArea')

for mysoup in ar_soups.find_all("li"):
    areaName = mysoup.find("a").text
    areaStr = str(areaName).strip()
    area.append(areaStr)
    areaID_text = mysoup.find("a")["href"]
    areamatchWord = re.findall(r"[a-z]+\d{2,}",areaID_text)
    areaID.append(areamatchWord)
        
del area[0]
del areaID[0]

areaList = list(zip(area,areaID))
areaDict = dict(areaList)    

movie.insert(0,'要看哪部電影')               #清單的預設字元
area.insert(0,'請選擇地區')                  #清單的預設字元
app = QtWidgets.QApplication(sys.argv)      # 視窗程式開始
Form = QtWidgets.QWidget()                  # 放入基底元件
Form.setWindowTitle('電影場次快搜器') 
Form.resize(400, 700)
Form.setStyleSheet('background:#00BFFF;')  # 使用網頁 CSS 樣式設定背景
box1 = QtWidgets.QComboBox(Form)           # 加入下拉選單
box1.addItems(movie)                       # 加入選項
box1.setGeometry(55,50,300,40)
box1.currentIndexChanged.connect(_show)
box1.setStyleSheet('background:#F8F8FF;')
box2 = QtWidgets.QComboBox(Form)           # 加入下拉選單
box2.addItems(area)                        # 加入選項
box2.setGeometry(55,100,300,40)
box2.currentIndexChanged.connect(_search)
box2.setStyleSheet('background:#F8F8FF;')

listwidget = QtWidgets.QListWidget(Form)
listwidget.setGeometry(55,180,300,450)
listwidget.setStyleSheet('background:#F8F8FF;')
Form.show()                               # 顯示元件
sys.exit(app.exec_())
