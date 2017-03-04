import json
import re
import io
import os
import requests
import time
import random
from bs4 import BeautifulSoup

class FileReader:
    def Read(self, fileName):
        f = io.open(fileName, "r")
        f.seek(0, 2)
        fileLength = f.tell()
        f.seek(0, 0)
        s = f.read(fileLength)
        f.close()
        return s

class FilmReader:
    def Read(self, filmYearFile):
        fr = FileReader()
        s = fr.Read(filmYearFile)
        filmsDic = json.loads(s)
        films = []
        for key in filmsDic:
            value = filmsDic[key]
            bytesValue = value.encode()
            films.append({"url" : key, "name" : bytesValue.decode("utf8")})
        
        return films

class Crawer:
    def Read(self, url):
        r = requests.get(url)

        soup = BeautifulSoup(r.text, "html5lib")

        con = soup.find(id="info")
        return con.get_text()

class ResultReader:
    def Craw(self, filePath, targetPath):
        fr = FilmReader()
        filmInfos = fr.Read(filePath)
        c = Crawer()
        codePattern = u".*/(\d+)/$"
        codePattern = re.compile(codePattern)
        for film in filmInfos:
            code = codePattern.findall(film["url"])
            path = os.path.join(targetPath, code[0] + ".txt")
            try:
                f = io.open(path, "w")
                text = c.Read(film["url"])
                bytesText = text.encode()
                f.write(film["name"]+"\n")
                f.write(text)
                f.close()
                time.sleep(random.uniform(1, 3))
            except:
                i = 1 + 1
            else:
                print(film["name"])


    def Read(self, resultPath, targetPath):
        filePattern = u"^result_(\d+)_\.json$"
        filePattern = re.compile(filePattern)
        for rt, dirs, files in os.walk(resultPath):
            for f in files:
                year = filePattern.findall(f)
                year = year[0]
                path = os.path.join(targetPath, year)
                try:
                    os.mkdir(path)
                except:
                    i = 1 + 1
                self.Craw(os.path.join(resultPath, f), path)
                
                

a = ResultReader()
a.Read("F:\\result", "F:\\pytest\\test")
# a = FilmReader()
# films = a.Read("F:\\result\\result_2010_.json")
# for info in films:
#     print(info)
