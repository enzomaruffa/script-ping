# -*- coding: utf-8 -*-
# Multiping lib supports more than one IP at once, but this script uses only one.


from multiping import MultiPing
from multiping import multi_ping
import twitter_interface
import time
import datetime
import math

# -------------------------------------------
# Result class
class Result:
	
	def __init__(self, host, date, ping, level):
		self.host = host
		self.date = date
		self.ping = ping
		self.level = level

	def display(self):
		print ("Pinging", self.host, ". Ping is", format(self.ping, '.6f'), "ms at", self.date, ". Threat level:", self.level) 


# Write result in file
def write(file, result):
	csv_string = result.host + ";" + str(format(result.ping, '.6f')) + ";" + str(result.date) + ";" + str(result.level) + "\n"
	file.write(csv_string)


# -------------------------------------------
# 'IMPORTANT' GLOBAL VARS
ping_address = "google.com"
ping_delay = 0.5

# ISDOWN VARS, used to check if internet is down and calculate how long it has been down.
is_down = False
last_down = datetime.datetime.now()

# COUNTERS
bad_pings = 0 # Counts how many bad pings (>50) since last tweet.

while True:
	responses, no_responses = multi_ping([ping_address], timeout=1, retry=2,ignore_lookup_errors=True)
	
	date = datetime.datetime.now()

	# Basically if internet is down
	if no_responses:
		print ("Could not find IP. Maybe you have no connection?")
		# Write ping as -1 if down. Threat level = 9.
		result = Result(no_responses[0], date, -1, 9)
		
		# Write even if internet is down
		file = open("allping.txt", "a") 
		write(file, result)
		file.close();

		# Updates down status
		if not is_down:
			is_down = True
			last_down = datetime.datetime.now()
		time.sleep(ping_delay)

	else:
		for addr, rtt in responses.items():
		
			rtt = round(rtt, 6)

			if is_down:
				is_down = False

				# Gets current time and calculates downtime
				now = datetime.datetime.now()
				downtime = (now - last_down).total_seconds() 
				
				# Write to file
				internet_file = open("no_internet_time.txt", "a")				
				internet_file.write(str(now) + ";" + str(downtime) + "\n")
				internet_file.close()

				twitter_interface.tweet_downtime(last_down, downtime)

			file = open("allping.txt", "a")

			bin_limit = 50 # Defines how "large" is a threat level
			threat_level = math.floor((rtt*1000)/50)
			
			result = Result(addr, date, rtt*1000, threat_level)
			result.display()
			
			# If ping is higher than 100ms
			if (result.ping >= 100):
				bad_pings += 1 
				# If last tweet was before 5 minutes ago, then tweet
				if twitter_interface.check_last_tweet():
					twitter_interface.tweet_bad_ping(result, bad_pings)
					bad_pings = 0

			write(file, result)
			file.close();
		
	#Default delay entre pings	
	time.sleep(ping_delay)





