### MangaScraper
 A Manga Scraping Website which can download manga for Mangakatana. There is a lot of excess extra output in the terminal currently. To run the program, run mangaScraper.py

### installation
Into your environment, install requests, beautifulsoup4, and selenium
ex.
pip install requests, beautifulsoup4, selenium

For selenium, also install a chrome driver that matches your chrome version at https://chromedriver.chromium.org/downloads and add it's executable to your system's path in environment variables.

### Other Details
- selectors use beautifulsoup4, with documentation at https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- use Selenium (S) as the method when the images are on the website are loaded using JavaScript, otherwise Bs4 is faster
- choosing between 'src' vs 'data-src' as the img source can be quite arbitrary, I recommended testing both
- info.txt is a collection of selectors for mangawebsites I've tested