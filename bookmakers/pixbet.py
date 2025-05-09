from bs4 import BeautifulSoup
import requests

competition_urls = {
		'football':
		{
			"ligue1": "https://pixbet.com/prejogo/#league/48",
			"liga": "",
			"bundesliga": "",
			"premier-league": "",
			"serie-a": "",
			"primeira": "",
			"serie-a-brasil": "",
			"a-league": "",
			"bundesliga-austria": "",
			"division-1a": "",
			"super-lig": "",
		},
		'basketball':
		{
			"nba": "",
			"euroleague": "",
		}
}

def get_page(competition):
	if (competition["sport"] in competition_urls and competition["competition"] in competition_urls[competition["sport"]]):
		url = competition_urls[competition["sport"]][competition["competition"]]
	else:
		return None
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
	print(response.content)
	html = BeautifulSoup(response.content, 'html.parser')
	return html

def get_games(competition):
	html = get_page(competition)	
	games = []
	games_els = html.select(".odds_tr")
	

	for game in games_els:
		
		odd_els = game.select(".oddValue")
		odds = []

		if (len(odd_els) == 1):
			continue
		
		for odd_el in odd_els:						
			odds.append(float(odd_el.text.replace(",", ".")))

		
		team1 = "".join(game.select(".competitor1")[0].text.split())
		team2 = "".join(game.select(".competitor2")[0].text.split())	



		print(team1)

		games.append({
			'team1': team1,
			'team2': team2,
			'odds': odds
		})

	
	return games




						
		
		


		
        

