#!/usr/bin/env python3
# multidownloadXkcd.py - Downloads comics from manga websites

import requests, os, bs4, threading, re
import comic

def downloadXkcd(startComic, endComic):
    for urlNumber in range(startComic, endComic):
        #download page
        print('Downloading page https://ww5.mangakakalot.tv/chapter/manga-kd987738/chapter-%s...' % (urlNumber))
        res = requests.get('https://ww5.mangakakalot.tv/chapter/manga-kd987738/chapter-%s' % (urlNumber))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features='html.parser')

        noHomeChapter = "chapter%s" % urlNumber
        os.makedirs('NoHome/' + noHomeChapter, exist_ok=True)


        #find URL of img
        comicElem = soup.select('#vungdoc img')
        if comicElem == []:
            print('Could not find comic image.')
        else:
            i = 0
            for element in comicElem:
                comicUrl = element.get('data-src')
                #Download the image
                print('Downloading image %s...' % (comicUrl))
                res = requests.get(comicUrl)
                res.raise_for_status()

                #save to xkcd
                imageFile = open(os.path.join('NoHome/' + noHomeChapter, "%s.jpg" % i), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                i += 1

#User Interface
while(True):
    print("Type 1 if you are downloading from MangaKatana and 2 if from MangaKakalot")
    website = input()
    if(website.strip() != "1" and website.strip() != "2"):
        print("Input format wrong, let's try that again!")
        continue
    print("Which chapters do you want to download? Give in form num1-num2, ex. 1-20")
    range = input()
    if(re.search("\d+-\d+", range.strip())==None):
        print("Input format wrong, let's try that again!")
        continue
    numbers = re.findall("\d+", range.strip())
    if(int(numbers[1]) < int(numbers[0])):
        print("Range is not reasonable, let's try that again!")
        continue
    print("Please give the path to download the manga, or just the foldername if in the current working directory")
    path = input()
    print("Please give the link to the manga. Ex. https://mangakatana.com/manga/the-horizon.25833")
    link = input()
    comicData = comic.Comic(website, range, path, link)
    print("Ok nice")


os.makedirs('NoHome', exist_ok=True)

