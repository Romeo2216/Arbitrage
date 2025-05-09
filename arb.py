from difflib import SequenceMatcher
import log
import numpy as np





mismatch_pairs = [
	["MelbourneCity", "MelbourneVictory"],
	["MelbourneCityFC", "MelbourneVictoryFC"]
]

def str_similarity(a, b):
	return SequenceMatcher(None, a, b).ratio()

def get_game(game, others):
	if (len(others) == 0 or game == None):
		return None
	m = 0
	m_obj = None
	for other in others:
		sim = str_similarity(game['team1'], other['team1']) + str_similarity(game['team2'], other['team2'])
		if (sim > m):
			m = sim
			m_obj = other

	tolerance = 0.60
	if (str_similarity(game['team1'], m_obj['team1']) < tolerance):
		return None
	if (str_similarity(game['team2'], m_obj['team2']) < tolerance):
		return None
	for mismatch in mismatch_pairs:
		if ([game['team1'], m_obj['team1']] == mismatch or [m_obj['team1'], game['team1']] == mismatch):
			return None
		if ([game['team2'], m_obj['team2']] == mismatch or [m_obj['team2'], game['team2']] == mismatch):
			return None
	return m_obj

def arb3(a, n, b):
	return (1 - (1/a + 1/n + 1/b)) * 100

def arb2(a, b):
	return (1 - (1/a + 1/b)) * 100

def dec_to_base(num, base):
	base_num = ""
	while (num > 0):
		dig = int(num % base)
		if (dig < 10):
			base_num += str(dig)
		else:
			base_num += chr(ord('A')+dig-10)
		num //= base
	base_num = base_num[::-1]
	return base_num

def arb_football(games):

	bookmaker_name = ['winamax','pmu','betclic','zebet','netbet']
	bookmaker_stat = [0]*5

	odd1 = []
	odd2 = []
	odd3 = []
	game_list = []


	nb_bookmakers = len(games)
	combinations = nb_bookmakers ** 3
	log.log("-- Arbitrage on: ")
	for game in games:
		if (len(games[game]['odds']) < 3):
			nb_bookmakers = nb_bookmakers - 1
			combinations = nb_bookmakers ** 3
			continue

		odd1.append(games[game]['odds'][0])
		odd2.append(games[game]['odds'][1])
		odd3.append(games[game]['odds'][2])
		game_list.append(game)

		log.log("{:10}: {} - {} @{}/{}/{}".format(game, games[game]['team1'], games[game]['team2'], games[game]['odds'][0], games[game]['odds'][1], games[game]['odds'][2]))
	#log.log("{} combinations possible --".format(combinations))

	odd1 = np.array(odd1)
	odd2 = np.array(odd2)
	odd3 = np.array(odd3)
	

	C1 = np.argmax(odd1)
	C2 = np.argmax(odd2)
	C3 = np.argmax(odd3)

	profit = arb3(
				odd1[C1],
				odd2[C2],
				odd3[C3],
		)
	
	

	log.log("({:10}/{:10}/{:10}) {:.2f}%".format(			
			game_list[C1],
			game_list[C2],
			game_list[C3],
			profit
		))

	return bookmaker_stat

	"""

	profitMax = -100
	combine = ""
	a1 = ""
	a2 = ""
	a3 = ""

	for i in range(combinations):
		
		combination = str(dec_to_base(i, nb_bookmakers)).zfill(3)
		b1 = list(games.keys())[int(combination[0])]
		b2 = list(games.keys())[int(combination[1])]
		b3 = list(games.keys())[int(combination[2])]
		profit = arb3(
				games[b1]['odds'][0],
				games[b2]['odds'][1],
				games[b3]['odds'][2],
		)

		if (profit > profitMax):
			profitMax = profit
			combine = combination
			a1 = b1
			a2 = b2
			a3 = b3

	log.log("{}: ({:10}/{:10}/{:10}) {:.2f}%".format(
			" ".join(combine.split()),
			a1,
			a2,
			a3,
			profitMax
		))
	
	for i in range(len(bookmaker_name)):

		if bookmaker_name[i] == a1:
			bookmaker_stat[i] += 1

		if bookmaker_name[i] == a2:
			bookmaker_stat[i] += 1

		if bookmaker_name[i] == a3:
			bookmaker_stat[i] += 1

	return bookmaker_stat
	"""

		

"""
		if (profit > 0):
			log.log("FOUND!!!!")
			stakes = get_stakes3(
				games[b1]['odds'][0],
				games[b2]['odds'][1],
				games[b3]['odds'][2],
				10)
			log.discord("Abritrage found for **{}**-**{}** with **{}/{}/{}** with odds {}/{}/{}: {:.2f}%".format(
				games[b1]['team1'],
				games[b1]['team2'],
				b1,
				b2,
				b3,
				games[b1]['odds'][0],
				games[b2]['odds'][1],
				games[b3]['odds'][2],
				profit
			))
			log.discord("> Stakes: **{}**@{} on {} for A, **{}**@{} on {} for N, **{}**@{} on {} for B".format(
				stakes['rounded'][0],
				games[b1]['odds'][0],
				b1,
				stakes['rounded'][1],
				games[b2]['odds'][1],
				b2,
				stakes['rounded'][2],
				games[b3]['odds'][2],
				b3,
			))
		log.log("{}: ({:10}/{:10}/{:10}) {:.2f}%".format(
			" ".join(combination.split()),
			b1,
			b2,
			b3,
			profit
		))
"""
