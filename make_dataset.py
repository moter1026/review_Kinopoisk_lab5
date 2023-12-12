import os
from bs4 import BeautifulSoup
from lxml import html
import requests
import math
from fake_useragent import UserAgent
import time
import random
import json


urlKin = "https://www.kinopoisk.ru/film/"
urlRew = "/reviews/ord/date/status/all/perpage/200/page/"
urlNums = [435,326,448,1072974, 258687, 361]

with open('films.json') as obj:
    templates = json.load(obj)
keys = templates.keys()
for key in keys:
    urlNums.append(int(key))

indexGood = 0
indexBad = 0
indexPage = 1
indexSite = 0

if (os.path.exists("data.txt")):
    with open("data.txt", "r") as dataFile:
        lines = dataFile.readlines()
        indexGood = int(lines[0][14: -2])
        indexBad = int(lines[1][12: -2])
        indexPage = int(lines[2][12: -2])
        indexSite = int(lines[3][12: -2])


rnd = random.randrange(1, 25)
print(rnd)
time.sleep(rnd)
req1 = requests.get(urlKin + str(urlNums[indexSite]) + urlRew + str(indexPage), headers={"User-Agent":UserAgent().chrome})
src = BeautifulSoup(req1.text, "lxml")
maxCountOfReviews = int(src.find("li",attrs={"class":"all"}).text[6:])
countPage = math.ceil(maxCountOfReviews/200)

while ( indexBad < 1000 or indexGood < 1000 ) :
    nameOfFilm = src.find("a",attrs={"class":"breadcrumbs__link"}).text
    print(nameOfFilm)
    
    reviewsGood = src.find_all("div", attrs={"class":"good"})
    reviewsBad = src.find_all("div", attrs={"class":"bad"})
    
    if not os.path.isdir("dataset"):
        os.mkdir("dataset")
    os.chdir("dataset")
    
    if indexGood < 1000:
        if not os.path.isdir("good"):
            os.mkdir("good")
        os.chdir("good")
        fileName = '';
        
        for review in reviewsGood:
            fileName = str(indexGood + 1).zfill(4)+".txt"
            with open(fileName, "w+") as textFile:
                textFile.write(nameOfFilm)
                textFile.write("\n\n")
                rew = review.next_element.next_element.next_element.next_element.next_sibling.next_element.next_element.next_element.next_element.next_element.next_element.next_element
                rewText = rew.text
                if rew.text.find("∞") != -1:
                    rewText = rew.text.replace("∞", "бесконечность")
                textFile.write(rewText)
            indexGood+=1
        os.chdir("../")

    if indexBad < 1000:
        if not os.path.isdir("bad"):
            os.mkdir("bad")
        os.chdir("bad")
        for review in reviewsBad:
            fileName = str(indexBad + 1).zfill(4)+".txt"
            with open(fileName, "w+") as textFile:
                textFile.write(nameOfFilm)
                textFile.write("\n\n")
                rew = review.next_element.next_element.next_element.next_element.next_sibling.next_element.next_element.next_element.next_element.next_element.next_element.next_element
                rewText = rew.text
                if rew.text.find("∞") != -1:
                    rewText = rewText.replace("∞", "бесконечность")
                textFile.write(rewText)
            indexBad+=1
        os.chdir("../")
    
    
    
    if(indexBad < 1000 or indexGood < 1000):
        if(indexPage < countPage):
            indexPage += 1
            os.chdir("../")
            with open("data.txt", "w+") as dataFile:
                dataFile.write("Good reviews: " + str(indexGood) + ";\n")
                dataFile.write("Bad reviews: " + str(indexBad) + ";\n")
                dataFile.write("index page: " + str(indexPage) + ";\n")
                dataFile.write("index site: " + str(indexSite) + ";\n")
            rnd = random.randrange(6, 15)
            print(rnd)
            time.sleep(rnd)
            req1 = requests.get(urlKin + str(urlNums[indexSite]) + urlRew + str(indexPage), headers={"User-Agent":UserAgent().chrome})
            src = BeautifulSoup(req1.text, "lxml")
        else:
            indexSite += 1
            indexPage = 1
            os.chdir("../")
            with open("data.txt", "w+") as dataFile:
                dataFile.write("Good reviews: " + str(indexGood) + ";\n")
                dataFile.write("Bad reviews: " + str(indexBad) + ";\n")
                dataFile.write("index page: " + str(indexPage) + ";\n")
                dataFile.write("index site: " + str(indexSite) + ";\n")
            rnd = random.randrange(6, 15)
            print(rnd)
            time.sleep(rnd)
            req1 = requests.get(urlKin + str(urlNums[indexSite]) + urlRew + str(indexPage), headers={"User-Agent":UserAgent().chrome})
            src = BeautifulSoup(req1.text, "lxml")
            maxCountOfReviews = int(src.find("li",attrs={"class":"all"}).text[6:])
    else:
        os.chdir("../")
        with open("data.txt", "w+") as dataFile:
            dataFile.write("Good reviews: " + str(indexGood) + ";\n")
            dataFile.write("Bad reviews: " + str(indexBad) + ";\n")
            dataFile.write("index page: " + str(indexPage) + ";\n")
            dataFile.write("index site: " + str(indexSite) + ";\n")
    

    