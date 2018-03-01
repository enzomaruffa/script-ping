# -*- coding: utf-8 -*-
# A lib de multiping funciona para pingar vários endereços, mas esse programa funciona com apenas um


from multiping import MultiPing
import time
import datetime

# -------------------------------------------
# Classe de resultado
class Result:
	
	def __init__(self, host, date, ping, level):
		self.host = host
		self.date = date
		self.ping = ping
		self.level = level

	def display(self):
		print ("Pinging ", self.host, ". Ping is", format(self.ping, '.6f'), "s at ", self.date, ". Threat level: ", self.level) 


# Função para escrever um result em um arquivo
def write(file, result):
	csv_string = result.host + ";" + str(format(result.ping, '.6f')) + ";" + str(result.date) + ";" + str(result.level) + "\n"
	file.write(csv_string)

def check_last_tweet():
	now = datetime.datetime.now()
	if last_tweet == None or (last_tweet - now).total_minutes() >= 5:
		return True
	return False

# -------------------------------------------

shitty_ping = False;
ping_address = "google.com"
ping_delay = 0.5
bad_pings = 0 # Guarda os pings ruins desde o último tweet
last_tweet = None # Data do último tweet

while True:
	#Se for um ping ruim, escreve que merda
	if shitty_ping:
		print("Well, fuck. That's a shitty ping.")
		shitty_ping = False

	#Editar aqui para adicionar mais IPs NÃO RECOMENDADO
	mp = MultiPing([ping_address])
	mp.send()
	responses, no_responses = mp.receive(1)
	
	date = datetime.datetime.now()

	if no_responses:
		print ("NETWORK DOWN GOING DARK BRB GONNA HIDE FOR 5 SECONDS")
		# Escreve com ping 0 quando cai
		result = Result(no_responses[0], date, 0, 5)
		
		# Escreve caso não receba
		file = open("allping.txt", "a") 
		write(file, result)
		file.close();
		
		time.sleep(ping_delay)

	else:
		for addr, rtt in responses.items():
			file = open("allping.txt", "a")
		
			
			rtt = round(rtt, 6)
			#Ping maior que 150
			if rtt >= 0.15:
				result = Result(addr, date, rtt, 3)
				result.display()	
				write(file, result)
				
				# Controle dos pings ruins e twitta caso ruim.
				bad_pings += 1 
				if check_last_tweet():
					#tweet(result, bad_pings)
					bad_pings = 0

				shitty_ping = True

			#Ping maior que 100
			elif rtt >= 0.100:
				result = Result(addr, date, rtt, 2)
				result.display()
				write(file, result)
				bad_pings += 1
				shitty_ping = True

			#Ping maior que 50
			elif rtt >= 0.05:
				result = Result(addr, date, rtt, 1)
				result.display()
				write(file, result)

			else:
				result = Result(addr, date, rtt, 0)
				result.display()
				write(file, result)

			file.close();
		
	#Default delay entre pings	
	time.sleep(ping_delay)




