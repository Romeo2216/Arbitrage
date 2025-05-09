from bs4 import BeautifulSoup
import requests
import json

competition_urls = {
		'football':
		{
			"ligue1": "https://www.betclic.fr/football-s1/ligue-1-uber-eats-c4",
			"liga": "https://www.betclic.fr/football-s1/espagne-liga-primera-c7",
			"bundesliga": "https://www.betclic.fr/football-s1/allemagne-bundesliga-c5",
			"premier-league": "https://www.betclic.fr/football-s1/angl-premier-league-c3",
			"serie-a": "https://www.betclic.fr/football-s1/italie-serie-a-c6",
			"primeira": "https://www.betclic.fr/football-s1/portugal-primeira-liga-c32",
			"serie-a-brasil": "https://www.betclic.fr/football-s1/bresil-serie-a-c187",
			"a-league": "https://www.betclic.fr/football-s1/australie-a-league-c1874",
			"bundesliga-austria": "https://www.betclic.fr/football-s1/autriche-bundesliga-c35",
			"division-1a": "https://www.betclic.fr/football-s1/belgique-division-1a-c26",
			"super-lig": "https://www.betclic.fr/football-s1/turquie-super-lig-c37",
		},
		'basketball':
		{
			"nba": "https://www.betclic.fr/basket-ball-s4/nba-c13",
			"euroleague": "https://www.betclic.fr/basket-ball-s4/euroligue-c14",
		}
}

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	
	return response.text

def get_games(competition):
	html = get_page(competition)

	split1 = html.split('<script id="ng-state" type="application/json">')[1]

	split2 = split1.split("</script></body></html>")[0]

	json_data = json.loads(split2)

	games = json_data.get(list(json_data.keys())[-2], []).get('response', []).get('payload',[]).get('matches', {})

	games_final = []
	
	
	for game in games:

		team1 = game.get('market', {}).get('mainSelections', '')[0].get('name', '')
		team2 = game.get('market', {}).get('mainSelections', '')[2].get('name', '')
		
		od1 = game.get('market', {}).get('mainSelections', '')[0].get('odds', '')
		od2 = game.get('market', {}).get('mainSelections', '')[1].get('odds', '')
		od3 = game.get('market', {}).get('mainSelections', '')[2].get('odds', '')

		odds = [od1, od2, od3]

		"""team = game.select(".contestant-1-label")
		

		odd_els = game.select(".oddValue")
		odds = []

		if (len(odd_els) == 1 or len(odd_els) == 0):				
				continue
		
		
		if (len(odd_els) == 2):
			if ("".join(team[0].text.split()) == "Nul"):
				odds.append(1)
			
		for odd_el in odd_els:						
			odds.append(float(odd_el.text.replace(",", ".")))

		if (len(odd_els) == 2):
			if ("".join(team[1].text.split()) == "Nul"):
				odds.append(1)
		
		names = game.select(".scoreboard_contestantLabel")			
		team1 = "".join(names[0].text.split())
		team2 = "".join(names[1].text.split())"""	
					
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
	print(games)