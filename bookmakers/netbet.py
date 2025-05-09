from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options

competition_urls = {
	'football': 
	{
		"ligue1": "https://www.netbet.fr/football/france/ligue-1-mcdonald-stm",
		"liga": "https://www.netbet.fr/football/espagne/laliga",
		"bundesliga": "https://www.netbet.fr/football/allemagne/bundesliga",
		"premier-league": "https://www.netbet.fr/football/angleterre/premier-league",
		"serie-a": "https://www.netbet.fr/football/italie/coupe-d-italie",
		"primeira": "https://www.netbet.fr/football/portugal/primeira-liga",
		"serie-a-brasil": "https://www.netbet.fr/football/bresil/brasileirao",
		"a-league": "https://www.netbet.fr/football/australie/a-league",
		"bundesliga-austria": "https://www.netbet.fr/football/autriche/bundesliga",
		"division-1a": "https://www.netbet.fr/football/belgique/pro-league",
		"super-lig": "https://www.netbet.fr/football/turquie/super-lig",
	},
	'basketball':
	{
		"nba": "https://www.netbet.fr/basketball/etats-unis/nba",
		"euroleague": "https://www.netbet.fr/basketball/coupes-d-europe/euroligue",
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

	games = html.select(".line-container")

	for game in games:

		odds = []

		odd = game.select(".container-odd-and-trend:not(.loading)")
		for od in odd:
			o = float(od.text)
			if o in odds:
				break
			odds.append(o)
			

		names = game.select(".vertically-centered")

		if len(names) != 2:
			continue

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