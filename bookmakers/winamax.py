from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options

competition_urls = {
	'football':
	{
		"ligue1": "https://www.winamax.fr/paris-sportifs/sports/1/7/4",
		"liga": "https://www.winamax.fr/paris-sportifs/sports/1/32/36",
		"bundesliga": "https://www.winamax.fr/paris-sportifs/sports/1/30/42",
		"premier-league": "https://www.winamax.fr/paris-sportifs/sports/1/1/1",
		"serie-a": "https://www.winamax.fr/paris-sportifs/sports/1/31/33",
		"primeira": "https://www.winamax.fr/paris-sportifs/sports/1/44/52",
		"serie-a-brasil": "https://www.winamax.fr/paris-sportifs/sports/1/13/83",
		"a-league": "https://www.winamax.fr/paris-sportifs/sports/1/34/144",
		"bundesliga-austria": "https://www.winamax.fr/paris-sportifs/sports/1/17/29",
		"division-1a": "https://www.winamax.fr/paris-sportifs/sports/1/33/38",
		"super-lig": "https://www.winamax.fr/paris-sportifs/sports/1/46/62",
	},
	'basketball':
	{
		"nba": "https://www.winamax.fr/paris-sportifs/sports/2/800000076/177",
		"euroleague": "https://www.winamax.fr/paris-sportifs/sports/2/800000034/153",
	}
}

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		return None
	
	service = Service("chromedriver-win64\chromedriver.exe")  # Ex : "C:/WebDriver/chromedriver.exe"
	driver = webdriver.Chrome(service=service)
	options = Options()
	options.add_argument("--headless")  # Active le mode headless
	options.add_argument("--disable-gpu")  # Optionnel, améliore la compatibilité
	options.add_argument("--no-sandbox")  # Optionnel, utile pour certains environnements

	service = Service("chromedriver-win64\chromedriver.exe")
	driver = webdriver.Chrome(service=service, options=options)

	driver.get(url)
	sleep(3)  # Wait for the page to load

	html = driver.page_source

	driver.quit()

	html = BeautifulSoup(html, 'html.parser')

	return html

def get_games(competition):

	games_final = []

	html = get_page(competition)
		
	games = html.select(".sc-bJoeBu")

	for game in games:

		odds = []

		odd = game.select(".sc-llILlE")
		for od in odd:
			o = float(od.text.replace(",", "."))
			odds.append(o)
			

		names = game.select(".sc-doOioq")
		
		team1 = names[0].text
		team2 = names[1].text
	
		games_final.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})

	
	return games_final

if __name__ == "__main__":	
	competition = {
		"sport": "football",
		"competition": "ligue1"
	}
	
	games = get_games(competition)
	
	for game in games:
		print(game)