#!/usr/bin/env python3
#scraper.py - holds the functions used in each thread of mangaScraper.py
import requests, os, bs4, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def downloadManga(startComic, endComic, comicObj):
    for number in range(startComic, endComic):
        #download page
        chapter = comicObj.chapters[number]
        url = chapter.get('href')
        print("Downloading page %s" % (url))
        if(comicObj.method == "S"):
            comicElem = getImagesSelenium(url, comicObj.chapImgSelector)
        else:
            comicElem = getImagesBs4(url, comicObj.chapImgSelector)
        source = comicObj.imageSource

        os.makedirs('%s/%s/ch.%s' % (comicObj.path, comicObj.title, comicObj.chapNums[number]) , exist_ok=True)
        #find URL of img
        if comicElem == []:
            print('Could not find comic image.')
        else:
            i = 0
            for element in comicElem:
                comicUrl = element.get(source)
                #Download the image
                print('Downloading image %s...' % (comicUrl))
                res = requests.get(comicUrl)
                res.raise_for_status()

                #save to folder
                imageFile = open(os.path.join('%s/%s/ch.%s/%s.jpg' % (comicObj.path, comicObj.title, comicObj.chapNums[number], i)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                i += 1

def getImagesSelenium(url, selector):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Initialize the webdriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    time.sleep(3)
    page_source = driver.page_source
    soup = bs4.BeautifulSoup(page_source, features='html.parser')
    comicElem = soup.select(selector)
    driver.quit()
    return comicElem

def getImagesBs4(url, selector):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='html.parser')
    comicElem = soup.select(selector)
    return comicElem