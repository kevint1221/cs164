## Kai Wen Tsai
## ktsai017
## UCR
## CS164 Networking
## 12/4/19

### this is a server program that simulate twitter fucntion, such as posting, subscribe to others
### see offline post etc...
### 
#### 1. open one terminal that run this program in python2
####        - python server.py
#### 2. open others terminal that telnet to the localhost with port 8888
####        - telnet localhost 8888

import socket
import sys
import time
from thread import *


HOST = ''	# Symbolic name meaning all available interfaces
PORT = 8888	# Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#reuse 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
	
print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

# list of all clients
clients = []

# list of user
users = []
# message of each user(two dimension) index_user, message_each_user
user_message = []
#new message to show unread message(two dimension) index_user, new_message_each_user
user_new_message = []
#user subscription,  index_user
user_sub = []   
#hashtag list
hash_tag = []
#hash_tag that stored in each hashtage list(two dimension) hashtag, messages_in_each_hashtag_list
hash_tag_list = []

data = 0

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('====================WELCOME TO THE SERVER======================================\n') #send only takes string
	conn.send('===============================================================================\n')
	conn.send('=====######====================##====##=======##===============================\n')
	conn.send('=======##===##=====##======##======######===######====####=====##===###========\n')
	conn.send('=======##====##===##=##===##===##====##=======##=====##==##====##=##===========\n')
	conn.send('=======##=====##=##== ##=##====##====##=#=====##=#===####======###=============\n')
	conn.send('=======##======##======##======##====###======###====#####=====##==============\n')
	conn.send('===============================================================================\n\n')
	conn.send('Enter your username: ')
	data = conn.recv(1024)
	
	#if new user
	current_user = -1
	process = 1
	superuser = 0
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		#Receiving from client
		#close the connection 
		if data[0:4] == "quit" or data[0:1] == "7":
			for member in clients:
				if conn == member:
					print 'removing from list'
					# del member
					clients.remove(member)

			break
		if (data[0:13] == 'administrator' and len(data)-2 == 13):
			process = 0
			conn.send('Enter your password: ')
			data = conn.recv(1024)
			
			conn.send("==============================ADMINITRATOR MODE===================================\n")
			conn.send("==================================================================================\n")
			superuser = 1
			process = 2

			




		if (process ==1):
			for index, member in enumerate(users):
				if (data == member): #if user already come before
					current_user = index
					user_new_message[current_user] = [] #clean up this user's old post


			if (current_user == -1): #if it is new user
				users.append(data)
				print 'found new user: ', users[len(users)-1]
				current_user = current_user+ len(users)
				#create space for new user
				user_message.append([])
				user_sub.append([])
				user_new_message.append([])

			#password doesn't matter in here	
			conn.send('Enter your password: ')
			password = conn.recv(1024)
			conn.send('\n')

			#found # of new message
			number_new_message = 0
			for i in range (len(user_sub[current_user])):  #loop in user's subscription
					for x in range(len(users)): #loop through all users
						if(user_sub[current_user][i] == users[x]): ## if user's subscription match the user list
							for j in range(len(user_new_message[x])): 
								number_new_message +=1

			conn.send('              YOU HAVE ')
			conn.send(str(number_new_message))
			conn.send(' NEW MESSAGE\n')
			process = 2 

		#enter the selection: process2
		elif(process == 2 and superuser == 0):
			time.sleep(0.5)
			conn.send('\n\n')
			conn.send('============================================================\n')
			conn.send('||    1) See offline message    ||\n')
			conn.send('||    2) Edit subscriptions     ||\n')
			conn.send('||    3) Post message           ||\n')
			conn.send('||    4) See your followers     ||\n')
			conn.send('||    5) Search hashtag         ||\n')
			conn.send('||    6) See your post          ||\n')
			conn.send('||    7) Logout                 ||\n\n')
			conn.send('      SELECT MENU OPTION: ')
			process = 3
		##choose the selection: process 3
		elif(process == 2 and superuser ==1):
			conn.send('============================================================\n')
			conn.send('||    1) See messagecount since server started    ||\n\n')
			conn.send('      SELECT MENU OPTION: ')
			data = conn.recv(1024)
			if(data[0:1] == '1'):
				messagecount = 0
				for i in range(len(user_message)):
					for j in range(len(user_message[i])):
						messagecount+=1

				conn.send('\nTHERE ARE ')
				conn.send(str(messagecount))
				conn.send(' MESSAGES COUNTED SINCE SERVER STARTED\n\n\n')
				time.sleep(1)
		elif(process ==3):
			data = conn.recv(1024)
			if(data[0:1] == '1'): #see offline message
				conn.send('\n\n            YOUR OFFLINE MESSAGE BOX\n')
				conn.send('            ========================\n\n')
				for i in range (len(user_sub[current_user])):  #loop in user's subscription
					for x in range(len(users)): #loop through all user
						if(user_sub[current_user][i] == users[x]): ## if user's subscription match the user list
							conn.send('\nMESSAGE FROM: ')
							conn.send(users[x])
							for j in range(len(user_new_message[x])): 
								conn.send(user_new_message[x][j]) #print all new message out
								conn.send('============================================================\n')
				time.sleep(0.5)
				conn.send('\n')
			
			elif(data[0:1] == '3'): #post message
				message = "hi"
				conn.send('\n\n								Type cancel to go back:\n')
				conn.send('    ENTER MESSAGE:\n')
				message_length = 150
				while(message_length > 140):
					message = conn.recv(1024)
					if (len(message) > 140):
						conn.send('\n\n								Type cancel to go back:\n')
						conn.send("    You enter too many character!!!\n")
						conn.send("    ENTER MESSAGE AGAIN:\n")
					else:
						message_length = 10
				if(message[:-2] != 'cancel' and len(message) != 6):
					user_message[current_user].append(message)
					user_new_message[current_user].append(message)
					conn.send("\n    ENTER HASHTAG FOR THIS POST:\n")
					hashtag = conn.recv(1024)
					if (hashtag not in hash_tag):
						hash_tag.append(hashtag)
						hash_tag_list.append([])
						hash_tag_list[-1].append(message)
					else:
						for i in range(len(hash_tag)): ##find the hashtag
							if (hashtag == hash_tag[i]):
								hash_tag_list[i].append(message) ##add hashtag to the list
								break
					conn.send("Message posted!")

				time.sleep(0.2)
			elif(data[0:1] == '2'):
				conn.send('\n\n								Type cancel to go back:\n')
				conn.send('||    1) Add subscription       ||\n')
				conn.send('||    2) Drop subscription      ||\n')
				message = conn.recv(1024)
				if(message[:-2] != 'cancel' and len(message)-2 != 6):
					if (message[0:1] == '1'):
						conn.send('\n        CURRENT USER :\n')
						conn.send('==============================\n')

						for i in users:
							if (i != users[current_user]):
								conn.send('==    ')
								conn.send(i)
								conn.send('\n')
						conn.send('\n\n								Type cancel to go back:\n')		
						conn.send('    Which user you want to subscribe to?\n')
						select = conn.recv(1024)
						if(select[:-2] != 'cancel' and len(select)-2 != 6):
							##print(select[:len(select)-1])
							if (select[:len(select)]) in users: 
								user_sub[current_user].append(select[:len(select)]) ## receive message always has \n at the end
								conn.send('Added subscription successfully!\n')
							else:
								conn.send("User doesn't exist\n")
					elif(message[0:1] =='2'):
						conn.send('\n        YOUR CURRENT SUBSCRIPTIONS\n')
						for i in range (len(user_sub[current_user])):
								conn.send('==    ')
								conn.send(user_sub[current_user][i])
								conn.send('                 ||\n')
						conn.send('\n\n								Type cancel to go back:\n')			
						conn.send('    which user you want to delete?\n')
						select = conn.recv(1024)
						if(select[:-2] != 'cancel' and len(select)-2 != 6):
							if (select[:len(select)]) in user_sub[current_user]:  ## 
								user_sub[current_user].remove(select[:len(select)])
								conn.send('Removed subscription successfully!\n')
							else:
								conn.send("User doesn't exist in your subscription\n")
			elif(data[0:1] == '5'):
				conn.send('\n\n								Type cancel to go back:\n')	
				conn.send("    Enter HASHTAG YOU WANT TO SEARCH:\n")
				hashtag = conn.recv(1024)
				if(hashtag[:-2] != 'cancel' and len(hashtag)-2 != 6):
					if hashtag in hash_tag:
						conn.send("    here is the hashtag found:\n")
						conn.send('=================================\n')
						for i in range (len(hash_tag)):
							if (hashtag == hash_tag[i]):
								for j in range (len(hash_tag_list[i])):
									conn.send('||    ')
									conn.send(hash_tag_list[i][j])
									conn.send('---------------------------||\n')
									
			elif(data[0:1] == '4'):
				conn.send("    HERE IS YOUR FOLLOWERS\n")
				conn.send('===============================\n')
				for i in range(len(user_sub)):
					if (users[current_user] in user_sub[i]):
						conn.send(users[i])

			process = 2

		#reply = 'OK...' + data
		if not data: 
			break

	#came out of loop
	conn.close()

#now keep talking with the client
while 1:
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	#start new thread 
	start_new_thread(clientthread ,(conn,))

s.close()