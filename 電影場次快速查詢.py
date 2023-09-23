import requests
from bs4 import BeautifulSoup
import re

url="http://www.atmovies.com.tw/movie/now/"
rq=requests.get(url)
rq.encoding="utf-8"
soup=BeautifulSoup(rq.text,"lxml")

soups=soup.find("ul",'filmListPA')
movie=[]
film_id=[]

for mysoup in soups.find_all("li"):
    movie.append(mysoup.find("a").text)
    filmtext=mysoup.find("a")["href"]
    matchWord=re.findall(r"[a-z]+\d{4,}",filmtext)
    film_id.append(matchWord)
    
    
movieList=list(zip(movie,film_id))
movieDict=dict(movieList)

movieGet=input("輸入你想看的電影:")
try:
    moviePost=(movieDict[movieGet])
    
except:
    print("沒有這部電影!")

area_url="http://www.atmovies.com.tw/showtime/"
area_rq=requests.get(area_url)
area_rq.encoding="utf-8"
ar_soup=BeautifulSoup(area_rq.text,"lxml")
area=[]
areaID=[]
ar_soups=ar_soup.find("ul",'theaterArea')

for mysoup in ar_soups.find_all("li"):
    areaName=mysoup.find("a").text
    areaStr=str(areaName).strip()
    area.append(areaStr)
    areaID_text=mysoup.find("a")["href"]
    areamatchWord=re.findall(r"[a-z]+\d{2,}",areaID_text)
    areaID.append(areamatchWord)
        
del area[0]
del areaID[0]

for areaStr in area:
    areaStr.strip()
    
    

areaList=list(zip(area,areaID))
areaDict=dict(areaList)    

areaGet=input("在哪個縣市看:")

try:
    areaPost=(areaDict[areaGet])
    
except:
    print("沒有這個縣市!")
    
search_movie=moviePost[0]
search_area=areaPost[0]

    
movie_url="http://www.atmovies.com.tw/showtime/"+search_movie+r"/"+search_area+r"/"

    
movie_rq=requests.get(movie_url)   
    

movie_rq.encoding="utf-8"
film_soup=BeautifulSoup(movie_rq.text,"lxml")

film_soups=film_soup.find("div",{'id':'filmShowtimeBlock'})

for mysoup in film_soups.find_all("ul"):     
    print(mysoup.find("li").text)
    
    
    for mysoups in mysoup.find_all('li')[1:]:
        print(mysoups.text)
        print('-'*20)



