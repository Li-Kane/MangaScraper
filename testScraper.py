#!/usr/bin/env python3
# multidownloadXkcd.py - Downloads comics from manga websites

import requests, os, bs4, threading, re
import comic

def downloadManga(startComic, endComic, comicObj):
    for number in range(startComic, endComic):
        #download page
        chapter = comicObj.chapters[number]
        print("Downloading page %s" % (chapter.get('href')))
        res = requests.get(chapter.get('href'))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features='html.parser')
        print("SOUP                   ")
        print(soup)
        os.makedirs('%s/%s/ch.%s' % (comicObj.path, comicObj.title, comicObj.chapNums[number]) , exist_ok=True)
        #find URL of img
        if(comicObj.website == "Mangakatana"):
            selector = '#imgs .wrap_img img'
        
        comicElem = soup.select(selector)
        print(comicElem)
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
                imageFile = open(os.path.join('%s/%s/ch.%s/' + "%s.jpg" % (comicObj.path, comicObj.title, comicObj.chapNums[number], i)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                i += 1

#Asks necessary questions
comicData = comic.Comic()
while(True):
    print("Type 1 if you are downloading from MangaKatana and 2 if from MangaKakalot")
    website = input()
    if(comicData.setWebsite(website)): continue
    print("Which chapters do you want to download? Give in form num1-num2, ex. 1-20 or 2.5-15.1")
    chpRange = input()
    if(comicData.setRange(chpRange)): continue
    print("Please give the path to place the manga folder, as an absolute or relative path (it will overwrite folders)")
    path = input()
    if(comicData.setPath(path)): continue
    print("Please give the link to the manga. Ex. https://mangakatana.com/manga/the-horizon.25833")
    link = input()
    if(comicData.setLink(link)): continue
    comicData.print()
    print("Do you want to merge images of a chapter together?")
    merge = input()
    if(comicData.setCombine(merge)): continue
    break

#Set variables and start download threads
downloadThreads = []
size = int(len(comicData.chapters))
if(size < 10):
    stepSize = 2
elif(size < 25):
    stepSize = 5
elif(size < 50):
    stepSize = 10
elif(size < 100):
    stepSize = 20
else:
    stepSize = int(size/5)

for i in range(0,size,stepSize):
    pass
    downloadThread = threading.Thread(target = downloadManga, args=(i, i+stepSize, comicData))
    downloadThreads.append(downloadThread)
    downloadThread.start()

#wait for all threads to end.
for downloadThread in downloadThreads:
    downloadThread.join()
print('Done.')

