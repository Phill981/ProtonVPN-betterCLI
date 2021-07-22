import sys
import os
from time import sleep
from random import randint

class Program():
	def __init__(self, username:str, path:str)->None:
			self.user = username
			self.ti = False
			self.p = False
			self.servers = path

	def login(self)->None:
		os.system(f"protonvpn-cli login {self.user}")

	def logout(self)->None:
		os.system("protonvpn-cli logout")

	def requestCommand(self)->None:
		while True:
			command = input(">>")
			if command == "help" or command == "h":
				self.help()
			elif command == "reconnect" or command == "r":
				self.reconnect()
			elif command == "disconnect" or command == "d":
				self.disconnect()
			elif command == "connect" or command == "c":
				self.connect()
			elif command == "quit" or command == "q":
				sys.exit()
			elif command == "clear" or command == "cl":
				self.clear()
			elif command == "logout" or command == "l":
				self.logout()
			elif command == "circuit":
				while self.p == False:
					self.port = input("tcp or udp?\n>>")
					if self.port == "tcp" or self.port == "udp":
						self.p = True
					else:
						print("please enter 'tcp' or 'udp'")

				while self.ti == False:
					try:
						self.changeTime = int(input("How long do you want to stay on each server?(seconds)\n>>"))
						self.ti = True
					except:
						print("Please enter a valid number")
				self.createCircuit()
			else:
				print("Command not found write ' help' or 'h' to see all commands")

	def help(self)->None:
		print("""This is a list of all commands:\n
			'help | h' displays this message\n
			'reconnect | r' reconnect with a new server\n
			'connect | c' connects the vpn to a server\n
			'disconnect | d' disconnects from the server\n
			'clear | cl' clears the display\n
			'logout | l' log you out of your account\n
			'circuit' create a rotating circuit
			""")

	def clear(self)->None:
		os.system("clear")
		try:
			os.system("protonvpn-cli s")
		except:
			raise "Looks like protonvpn-cli isn't installed on your system. Install it first and come back later"

	def  reconnect(self)->None:
		try:
			os.system("protonvpn-cli d")
			os.system("protonvpn-cli c")
		except:
                        raise "Looks like protonvpn-cli isn't installed on your system. Install it first and come back later"


	def connect(self)->None:
		try:
			os.system("protonvpn-cli c")
			os.system("protonvpn-cli s")
		except:
                        raise "Looks like protonvpn-cli isn't installed on your system. Install it first and come back later"

	def disconnect(self)->None:
		try:
			os.system("protonvpn-cli d")
		except:
                        raise "Looks like protonvpn-cli isn't installed on your system. Install it first and come back later"


	def createCircuit(self)->None:
		lastNum = randint(0, len(self.serverList))
		"Press 'str-c' to quit\n"
		while True:
			index = randint(1, len(self.serverList))
			if index == lastNum:
				index -= 1
			lastNum = index
			os.system("clear")
			os.system(f"protonvpn-cli c {self.serverList[index]} -p {self.port}")
			os.system("protonvpn-cli s")
			print(f"Connecting to new server in {self.changeTime} seconds")
			sleep(self.changeTime)
			os.system("protonvpn-cli d")

	def readServers(self):
		with open(self.servers) as file:
			self.serverList = [line.strip() for line in file.readlines()]

if __name__ == "__main__":
	if len(sys.argv) > 3:
		print("Too many arguments given: 3 required\nCommand should look like this \n\n 'python3 proton.py username path_to_serverlist'")
		sys.exit()
	elif len(sys.argv) < 3:
		print("Not enough arguments given: 3 required\nCommand should look like this \n\n 'python3 proton.py username path_to_serverlist'")
		sys.exit(1)
	else:
		pass
	username = sys.argv[-2]
	pathServerlist = sys.argv[-1]
	proton = Program(username, pathServerlist)
	proton.login()
	proton.readServers()
	proton.requestCommand()
