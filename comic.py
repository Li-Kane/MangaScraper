#!/usr/bin/env python3
# comic.py - holds the Comic class which contains necessary values for scraping as gathered from
# mangaScraper.py

import re, os, requests, bs4
class Comic():
    def __init__(self):
        pass

    def setLink(self, link):
        self.res = requests.get(link)
        if(not requests.codes.ok): raise ValueError("Cannot connect to link, check and try again")
        self.link = link
        
    def setSelectors(self, titleSelector, chapSelector, chapImgSelector, imageSource):
        self.titleSelector = titleSelector
        self.chapSelector = chapSelector
        self.chapImgSelector = chapImgSelector
        self.imageSource = imageSource
        self.getTitle()
    
    def getTitle(self):
        self.res.raise_for_status()
        soup = bs4.BeautifulSoup(self.res.text, features='html.parser')
        title = soup.select(self.titleSelector)
        self.title = title[0].string
    
    def setRange(self, range):
        pattern = r"((\d*\.)?\d+)-((\d*\.)?\d+)"
        match = re.match(pattern, range)
        if(not match):
            raise ValueError("Range input should be in form num1-num1, ex. 2-5")
        elif(float(match[1]) > float(match[3])):
            raise ValueError("2nd number in range should be bigger than the first")
        else:
            self.range = [match[1], match[3]]
    
    def getChapters(self):
        self.res.raise_for_status()
        soup = bs4.BeautifulSoup(self.res.text, features='html.parser')
        #find Chapters
        chapter = soup.select(self.chapSelector)
        smallPattern = r"Chapter 0*" + self.range[0]
        bigPattern = r"Chapter 0*" + self.range[1]
        numPattern = r" ((\d*\.)?\d+)"
        smallNumIdx = [idx for idx, item in enumerate(chapter) if re.search(smallPattern, item.string)]
        bigNumIdx = [idx for idx, item in enumerate(chapter) if re.search(bigPattern, item.string)]
        if(smallNumIdx == [] or bigNumIdx == []):
            raise IndexError("Range bounds are not within the manga chapters offerered")
        if(bigNumIdx[-1] == 0):
            self.chapters = chapter[smallNumIdx[-1]::-1]
        else:
            self.chapters = chapter[smallNumIdx[-1]:bigNumIdx[-1]-1:-1]
        #get a list of numbers associated with each chapter obj in chapters
        chapNums = [re.search(numPattern, item.string) for item in self.chapters]
        self.chapNums = [item.group(1) for item in chapNums]
    
    def setPath(self, path):
        os.makedirs(path, exist_ok=True)
        self.path = path

    def setScrapeMethod(self, method):
        method = method.strip().lower()
        if(method == "b" or method == "bs4"):
            self.method = "B"
        elif(method == "s" or method == "selenium"):
            self.method = "S"
        else:
            raise ValueError("Please respond with B or S")
    
    def print(self):
        print("You are downloading %s from chapters %0.2f-%0.2f" % (self.title, float(self.range[0]), float(self.range[1])))
        print(self.chapNums)
        for item in self.chapters:
            print(item.string)
        