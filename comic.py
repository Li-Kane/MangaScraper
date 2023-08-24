import re, os, requests, bs4

class Comic():
    def __init__(self):
        pass
        
    def setWebsite(self, website):
        website = website.strip()
        if(website != "1" and website != "2"):
            print("Website input should be 1 or 2")
            return True
        if(website == "1"): 
            self.website = "Mangakatana"
        else:
            self.website = "MangaKakalot"
        return False
    
    def setRange(self, range):
        pattern = r"((\d*\.)?\d+)-((\d*\.)?\d+)"
        match = re.match(pattern, range)
        if(not match):
            print("Range input should be in form num1-num1, ex. 2-5")
            return True
        elif(float(match[1]) > float(match[3])):
            print("2nd number in range should be bigger than the first")
            return True
        else:
            self.range = [match[1], match[3]]
        return False
    
    def setPath(self, path):
        try: 
            os.makedirs(path, exist_ok=True)
        except:
            print("Path cannot be made")
            return True
        self.path = path
        return False
    
    def setLink(self, link):
        try: 
            res = requests.get(link)
        except requests.exceptions.MissingSchema:
            print("Does not appear to be a link, try again!")
            return True
        if(not requests.codes.ok):
            print("Cannot connect to link, check and try again")
            return True
        if("manganato" in link):
            self.website = "Chapmanganato"
        #try:
        #   self.getTitle(res)
        #    self.getChapters(res)
        #except:
        #   print("Cannot get chapters, check and try again")
        #    return True
        self.getTitle(res)
        self.getChapters(res)
        self.link = link
        return False
    
    def getChapters(self, res):
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features='html.parser')
        #find Chapters
        if(self.website == "Mangakatana"):
            chapter = soup.select('.chapters .chapter a')
        elif(self.website == "Chapmanganato"):
            chapter = soup.select('.row-content-chapter .a-h a')
        else:
            chapter = soup.select('.chapter-list .row a')
        smallPattern = r"Chapter 0*" + self.range[0]
        bigPattern = r"Chapter 0*" + self.range[1]
        numPattern = r" ((\d*\.)?\d+)"
        smallNumIdx = [idx for idx, item in enumerate(chapter) if re.search(smallPattern, item.string)]
        bigNumIdx = [idx for idx, item in enumerate(chapter) if re.search(bigPattern, item.string)]
        if(smallNumIdx == [] or bigNumIdx == []):
            print("Range bounds are not within the manga")
            raise IndexError
        if(bigNumIdx[-1] == 0):
            self.chapters = chapter[smallNumIdx[-1]::-1]
        else:
            self.chapters = chapter[smallNumIdx[-1]:bigNumIdx[-1]-1:-1]
        #get a list of numbers associated with each chapter obj in chapters
        chapNums = [re.search(numPattern, item.string) for item in self.chapters]
        self.chapNums = [item.group(1) for item in chapNums]
        return False
    
    def getTitle(self, res):
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features='html.parser')
        if(self.website == "Mangakatana"):
            title = soup.select('#single_book .info .heading')
        elif(self.website == "Chapmanganato"):
            title = soup.select('.story-info-right h1')
        else:
            title = soup.select('.manga-info-top .manga-info-text h1')
        self.title = title[0].string

    def setCombine(self, combine):
        ifCombine = combine.strip().lower()
        if(ifCombine == "yes" or ifCombine == "y"):
            self.combine = True
            return False
        elif(ifCombine == "no" or ifCombine=="n"):
            self.combine = False
            return False
        else:
            print("Please respond with yes or no")
            return True
    
    def print(self):
        print("You are downloading %s from chapters %0.2f-%0.2f" % (self.title, float(self.range[0]), float(self.range[1])))
        print("Its path is %s" % self.path)
        #for item in self.chapters:
        #    print(item.string)