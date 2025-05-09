#import discord_notify as dn
from datetime import datetime
import os
import time
import sys
import config
import ssl
import logging

ssl._create_default_https_context = ssl._create_unverified_context

discord_waiting_time = 1

def init():
	global filename
	global last_discord_message
	last_discord_message = time.time()
	filename = str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".log"
	os.system("mkdir -p logs")
	with open(filename, "w") as file:
		pass


def log(message, end="\n"):
	with open(filename, 'a') as file:
		file.write(message + end)

"""
def discord(message):
	global last_discord_message
	print(message)
	try:
		while (time.time() - last_discord_message < discord_waiting_time):
			time.sleep(discord_waiting_time)
		last_discord_message = time.time()
		notifier = dn.Notifier(config.discord_url)
		notifier.send(message, print_message=False)
	except:
		log("Error: cannot send message on Discord: {}".format(sys.exc_info()[0]))

"""