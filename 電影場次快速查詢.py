'''
爬取開眼電影網的網站資料，快速查詢電影場次時間

'''
import requests
from bs4 import BeautifulSoup
import re

#爬取本期首輪電影的名稱與對應的ID，存成字典  
url = "http://www.atmovies.com.tw/movie/now/"
rq = requests.get(url)
rq.encoding="utf-8"
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

movieGet = input("輸入你想看的電影:")
try:
    moviePost = (movieDict[movieGet]) #輸入的電影名稱為movieDict的key，回傳對應的value
    
except:
    print("沒有這部電影!")

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

areaGet = input("在哪個縣市看:")

try:
    areaPost = (areaDict[areaGet]) #輸入的地區名為areaDict的key，回傳對應的value
    
except:
    print("沒有這個縣市!")
#取出電影、地區的ID，加到網址後面，requests到目標網頁
search_movie = moviePost[0]
search_area = areaPost[0]
   
movie_url = "http://www.atmovies.com.tw/showtime/"+search_movie+r"/"+search_area+r"/"    
movie_rq = requests.get(movie_url)   
movie_rq.encoding = "utf-8"
film_soup = BeautifulSoup(movie_rq.text,"lxml")

film_soups = film_soup.find("div",{'id':'filmShowtimeBlock'})

for mysoup in film_soups.find_all("ul"):     
    print(mysoup.find("li").text)
    
    
    for mysoups in mysoup.find_all('li')[1:]:  #印出影城場次時間
        print(mysoups.text)
        print('-'*20)




