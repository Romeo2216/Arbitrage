import bookmakers.winamax as winamax
import bookmakers.pmu as pmu
import bookmakers.betclic as betclic
import bookmakers.zebet as zebet
import bookmakers.netbet as netbet
import bookmakers.unibet as unibet
import arb
import sys
import log
import config
import traceback
from tqdm import tqdm


log.init()

progress = 0
for competition in tqdm(config.competitions):
	bookmaker_name = ['winamax','pmu','betclic','zebet','netbet','unibet']
	bookmaker_stat = [0]*len(bookmaker_name)
	bookmaker_spawn = [0]*len(bookmaker_name)
	
	progress += 1
	bookmakers = {}
	try:
		bookmakers['winamax'] = winamax.get_games(competition)
		bookmaker_spawn[0] += len(bookmakers['winamax'])
		log.log("winamax: " + str(bookmakers['winamax']))
	except:
		log.log("Cannot crawl winamax: " + traceback.format_exc())
		bookmaker_name.remove('winamax')	
	try:
		bookmakers['pmu'] = pmu.get_games(competition)
		bookmaker_spawn[1] += len(bookmakers['pmu'])
		log.log("pmu: " + str(bookmakers['pmu']))
	except:
		log.log("Cannot crawl pmu: " + traceback.format_exc())
		bookmaker_name.remove('pmu')
	try:
		bookmakers['betclic'] = betclic.get_games(competition)
		bookmaker_spawn[2] += len(bookmakers['betclic'])
		log.log("betclic: " + str(bookmakers['betclic']))
	except:
		log.log("Cannot crawl betclic: " + traceback.format_exc())
		bookmaker_name.remove('betclic')
	try:
		bookmakers['zebet'] = zebet.get_games(competition)
		bookmaker_spawn[3] += len(bookmakers['zebet'])
		log.log("zebet: " + str(bookmakers['zebet']))
	except:
		log.log("Cannot crawl zebet: " + traceback.format_exc())
		bookmaker_name.remove('zebet')
	try:
		bookmakers['netbet'] = netbet.get_games(competition)
		bookmaker_spawn[4] += len(bookmakers['netbet'])
		log.log("netbet: " + str(bookmakers['netbet']))
	except:
		log.log("Cannot crawl netbet: " + traceback.format_exc())
		bookmaker_name.remove('netbet')
	try:
		bookmakers['unibet'] = unibet.get_games(competition)
		bookmaker_spawn[5] += len(bookmakers['unibet'])
		log.log("unibet: " + str(bookmakers['unibet']))
	except:
		log.log("Cannot crawl unibet: " + traceback.format_exc())
		bookmaker_name.remove('unibet')	
	log.log("-- Competition: {} --".format(competition))


	
	
	for i in range (len(bookmaker_name)):
		if (len(bookmakers[bookmaker_name[i]]) != 0):
			for game in bookmakers[bookmaker_name[i]]:
				games = {}
				for bookmaker in bookmakers:
					try:
						g = arb.get_game(game, bookmakers[bookmaker])
						if (g):
							games[bookmaker] = g
					except:
						log.log("Error while retrieving games: {}".format(traceback.format_exc()))
				if (competition["sport"] == "football"):
					bookmaker_stat_temp = arb.arb_football(games)

					"""
					for j in range(len(bookmaker_name)):
						bookmaker_stat[j] += bookmaker_stat_temp[j]	
					"""
			

			break
	
log.log(str(bookmaker_name))


for i in range(len(bookmaker_name)):
	bookmaker_stat[i] = bookmaker_stat[i]/bookmaker_spawn[i]

log.log(str(bookmaker_stat))
