#!/usr/bin/env python3
# mangaScraper.py - Downloads comics from manga websites

import threading
import comic, scraper

#Asks necessary questions
comicData = comic.Comic()
print("Please give the link to the manga. Ex. https://mangakatana.com/manga/the-horizon.25833")
link = input()
comicData.setLink(link)

print("Please give the selector for the manga's title. For Mangakatana Ex: #single_book .info .heading")
titleSelector = input()
print("Please give the selector for the manga's chapter links. For Mangakatana Ex: .chapters .chapter a")
chapLinksSelector = input()
print("Please give the selector for the images in each chapter. For Mangakatana Ex: #imgs .wrap_img img")
imgSelector = input()
print("Do the images use data-src or src? (Try both if unsure)")
imgSrc = input()
comicData.setSelectors(titleSelector, chapLinksSelector, imgSelector, imgSrc)

print("Which chapters do you want to download? Give in form num1-num2, ex. 1-20 or 2.5-15.1")
chpRange = input()
comicData.setRange(chpRange)
comicData.getChapters()

print("Please give the path to place the manga folder, as an absolute or relative path (it will overwrite folders)")
path = input()
comicData.setPath(path)

print("Use bs4 or selenium to parse images (use Selenium if imgs are loaded by javascript)? B or S to choose.")
scraperMethod = input()
comicData.setScrapeMethod(scraperMethod)
comicData.print()

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
    downloadThread = threading.Thread(target = scraper.downloadManga, args=(i, i+stepSize, comicData))
    downloadThreads.append(downloadThread)
    downloadThread.start()

#wait for all threads to end.
for downloadThread in downloadThreads:
    downloadThread.join()
print('Done.')
