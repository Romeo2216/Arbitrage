from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options

 
competition_urls = {
	'football':
	{
		"ligue1": "https://www.unibet.fr/sport/football/france/ligue-1-mcdonalds?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"liga": "https://www.unibet.fr/sport/football/espagne/laliga?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"bundesliga": "https://www.unibet.fr/sport/football/allemagne/bundesliga?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"premier-league": "https://www.unibet.fr/sport/football/angleterre/premier-league?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"serie-a": "https://www.unibet.fr/sport/football/italie/serie-a?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"primeira": "https://www.unibet.fr/sport/football/portugal/liga-portugal?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"serie-a-brasil": "https://www.unibet.fr/sport/football/bresil/serie-a?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"a-league": "https://www.unibet.fr/sport/football/australie/a-league?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"bundesliga-austria": "https://www.unibet.fr/sport/football/autriche/bundesliga?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"division-1a": "https://www.unibet.fr/sport/football/belgique/pro-league?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
		"super-lig": "https://www.unibet.fr/sport/football/turquie/super-lig?filter=Top+Paris&subFilter=R%C3%A9sultat+du+match",
	},
	'basketball':
	{
		"nba": "",
		"euroleague": ""
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
	games = html.select(".eventcard--toplight")

	for game in games:
		odds = []
		
		odd = game.select(".oddbox-value")
		for od in odd:
			o = float(od.text.replace(",", "."))
			odds.append(o)
			

		team1 = game.select(".mr-5")[0].text
		team2 = game.select(".ml-5")[0].text

		games_final.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})

	
	return games_final
	
if __name__ == "__main__":
	competition = {
		"sport": "football",
		"competition": "liga"
	}
	games = get_games(competition)
	for game in games:
		print(game)
	

	





