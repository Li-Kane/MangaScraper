#!/usr/bin/env python3
# multidownloadXkcd.py - Downloads comics from manga websites

import threading
import comic, scraper

#Asks necessary questions
comicData = comic.Comic()
while(True):
    print("Please give the link to the manga. Ex. https://mangakatana.com/manga/the-horizon.25833")
    link = input()
    if(comicData.setLink(link)): continue
    print("Which chapters do you want to download? Give in form num1-num2, ex. 1-20 or 2.5-15.1")
    chpRange = input()
    if(comicData.setRange(chpRange)): continue
    print("Please give the path to place the manga folder, as an absolute or relative path (it will overwrite folders)")
    path = input()
    if(comicData.setPath(path)): continue
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
    downloadThread = threading.Thread(target = scraper.downloadManga, args=(i, i+stepSize, comicData))
    downloadThreads.append(downloadThread)
    downloadThread.start()

#wait for all threads to end.
for downloadThread in downloadThreads:
    downloadThread.join()
print('Done.')

