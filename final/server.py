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

# message of each user(two dimension)
user_message = []

user_new_message = []

user_sub = []

#index
hash_tag = []
#hash_tag stored
hash_tag_list = []


data = 0

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the server\n') #send only takes string
	conn.send('enter your username\n')
	data = conn.recv(1024)
	
	current_user = -1
	process = 1
	posted = 0

	
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		#Receiving from client
		if data[0:4] == "quit" or data[0:1] == "10":
			for member in clients:
				if conn == member:
					print 'removing from list'
					# del member
					clients.remove(member)

			break


		if (process ==1):
			for index, member in enumerate(users):
				
				if (data == member): #if user already come before
					current_user = index
					user_new_message[current_user] = [] #clean up this user's old post


			if (current_user == -1): #if it is new user
				users.append(data)
				print 'found new user: ', users[len(users)-1]
				current_user = current_user+ len(users)
				user_message.append([])
				user_sub.append([])
				user_new_message.append([])

			conn.send('enter your password\n')
			password = conn.recv(1024)
			conn.send('\n')

			#found # of new message
			number_new_message = 0
			for i in range (len(user_sub[current_user])):  #loop in user's subscription
					for x in range(len(users)): #loop through all user
						if(user_sub[current_user][i] == users[x]): ## if user's subscription match the user list
							for j in range(len(user_new_message[x])): 
								number_new_message +=1

			conn.send('you have ')
			conn.send(str(number_new_message))

			conn.send(' new message\n')

			process = 2 

		elif(process == 2):
			time.sleep(0.5)
			conn.send('\n\n')
			conn.send('============================================================\n')
			conn.send('    1) see offline message\n')
			conn.send('    2) edit subscriptions\n')
			conn.send('    3) post message\n')
			conn.send('    4) see your followers\n')
			conn.send('    5) hashtag search\n')
			conn.send('    6) see your post\n')
			conn.send('    10) logout\n')
			conn.send('    back to go back to menu at anytime\n')
			conn.send('select menu option: ')
			process = 3
		elif(process ==3):
			data = conn.recv(1024)
			if(data[0:1] == '1'): #see offline message
				conn.send('    YOUR OFFLINE MESSAGE BOX\n')
				for i in range (len(user_sub[current_user])):  #loop in user's subscription
					for x in range(len(users)): #loop through all user
						if(user_sub[current_user][i] == users[x]): ## if user's subscription match the user list
							conn.send('\nmessage from: ')
							conn.send(users[x])
							for j in range(len(user_new_message[x])): 
								conn.send(user_new_message[x][j]) #print all new message out


				time.sleep(0.5)
					#conn.send(user_message[current_user][i])
				conn.send('\n')
			
			elif(data[0:1] == '3'): #post message
				message = "hi"
				conn.send('    ENTER MESSAGE type cancel to go back:\n')
				message_length = 150
				while(message_length > 140):
					message = conn.recv(1024)
					if (len(message) > 140):
						conn.send("enter too many character!!!\n")
						conn.send("    REENTER MESSAGE or type cancel to go back:\n")
					else:
						message_length = 10
				if(message[:-2] == 'cancel'):
					break
				user_message[current_user].append(message)
				user_new_message[current_user].append(message)
				conn.send("enter hashtage for this post:\n")
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

				time.sleep(0.2)
			elif(data[0:1] == '2'):
				conn.send('    1) add subscription\n')
				conn.send('    2) drop subscription\n')
				message = conn.recv(1024)
				if (message[0:1] == '1'):
					conn.send('        current user :\n')
					for i in users:
						if (i != users[current_user]):
							conn.send('    ')
							conn.send(i)
							conn.send('\n')
					conn.send('which user you want to subscribe to?\n')
					select = conn.recv(1024)
					##print(select[:len(select)-1])
					if (select[:len(select)]) in users: 
						user_sub[current_user].append(select[:len(select)]) ## receive message always has \n at the end
						conn.send('added subscription successfully!\n')
					else:
						conn.send("user doesn't exist\n")


				elif(message[0:1] =='2'):
					conn.send('        your current subscription\n')
					for i in range (len(user_sub[current_user])):
							conn.send('    ')
							conn.send(user_sub[current_user][i])
							conn.send('\n')
					conn.send('which user you want to delete?\n')
					select = conn.recv(1024)
					if (select[:len(select)]) in user_sub[current_user]:  ## 
						user_sub[current_user].remove(select[:len(select)])
						conn.send('removed subscription successfully!\n')
					else:
						conn.send("user doesn't exist in your subscription\n")
			elif(data[0:1] == '5'):
				conn.send("enter the hashtag you want to search:\n")
				hashtag = conn.recv(1024)
				if hashtag in hash_tag:
					conn.send("    here is the hashtag found:\n")
					for i in range (len(hash_tag)):
						if (hashtag == hash_tag[i]):
							for j in range (len(hash_tag_list[i])):
								conn.send(hash_tag_list[i][j])
			elif(data[0:1] == '4'):
				conn.send("    HERE IS YOUR FOLLOWERS\n")
				for i in range(len(user_sub)):
					if (users[current_user] in user_sub[i]):
						conn.send(users[i])

			process = 2





		#reply = 'OK...' + data
		if not data: 
			break

		#conn.send(reply)
	
	#came out of loop
	conn.close()

#now keep talking with the client
while 1:
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	start_new_thread(clientthread ,(conn,))

s.close()