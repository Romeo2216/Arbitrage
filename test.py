from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options

service = Service("chromedriver-win64\chromedriver.exe")  # Ex : "C:/WebDriver/chromedriver.exe"
driver = webdriver.Chrome(service=service)
options = Options()
#options.add_argument("--headless")  # Active le mode headless
options.add_argument("--disable-gpu")  # Optionnel, améliore la compatibilité
options.add_argument("--no-sandbox")  # Optionnel, utile pour certains environnements

service = Service("chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://parisportif.pmu.fr/home/wrapper/events?tfrom=P0D&tto=P2D&fId=2&activeSportId=1&leagues=%5B123%5D")
sleep(5)  # Wait for the page to load

html = driver.page_source

print(html)

driver.quit()

html = BeautifulSoup(html, 'html.parser')
games = html.select(".sb-event-list__row sb-event-list__row--desktop ng-star-inserted")

for game in games:

    odds = game.select(".sb-event-list__selection__outcome-value ng-star-inserted")
    for odd in odds:
        od = float(odd.text.replace(",", "."))
        print(od)
        

    names = game.select(".sb-event-list__competitor sb-event-list__competitor--prematch")
    for name in names:
        print(name.text)

    

    
        
    

