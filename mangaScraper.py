#!/usr/bin/env python3
# multidownloadXkcd.py - Downloads comics from manga websites

import requests, os, bs4, threading

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
os.makedirs('NoHome', exist_ok=True)

#Create and start Thread objects
downloadThreads = []
for i in range(1,50,10):
    downloadThread = threading.Thread(target = downloadXkcd, args=(i, i+9))
    downloadThreads.append(downloadThread)
    downloadThread.start()

#wait for all threads to end.
for downloadThread in downloadThreads:
    downloadThread.join()
print('Done.')