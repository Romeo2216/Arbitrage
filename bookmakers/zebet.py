from bs4 import BeautifulSoup
import requests

competition_urls = {
	'football':
	{
		"ligue1": "https://www.zebet.fr/paris-football/france/ligue-1-mcdonalds",
		"liga": "https://www.zebet.fr/paris-football/espagne/laliga",
		"bundesliga": "https://www.zebet.fr/paris-football/allemagne/bundesliga-1",
		"premier-league": "https://www.zebet.fr/paris-football/angleterre/premier-league",
		"serie-a": "https://www.zebet.fr/paris-football/italie/serie-a",
		"primeira": "https://www.zebet.fr/paris-football/portugal/liga-portugal",
		"serie-a-brasil": "https://www.zebet.fr/paris-football/bresil/d1-bresil",
		"a-league": "https://www.zebet.fr/paris-football/australie/d1-australie",
		"bundesliga-austria": "https://www.zebet.fr/paris-football/autriche/d1-autriche",
		"division-1a": "https://www.zebet.fr/paris-football/belgique/d1-belgique",
		"super-lig": "https://www.zebet.fr/paris-football/turquie/d1-turquie",
	},
	'basketball':
	{
		"nba": "https://www.zebet.fr/fr/competition/206-nba",
		"euroleague": "https://www.zebet.fr/fr/competition/12044-euroligue",
	}
}

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	html = BeautifulSoup(response.content, 'html.parser')
	return html

def get_games(competition):
	html = get_page(competition)
	games = []
	game_elements = html.select(".psel-event")
	for el in game_elements:

		name = el.select(".psel-opponent__name")

		if len(name) != 2:
			continue		

		od = el.select(".psel-market__outcome")

		team1 = name[0].text
		team2 = name[1].text
		odds = []

		for _ in od:
			odds.append(float(_.text.replace(",", ".")))

		games.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})
	return games

if __name__ == "__main__":
	competition = {
		"sport": "football",
		"competition": "ligue1"
	}
	games = get_games(competition)
	for game in games:
		print(game)