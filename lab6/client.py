import socket	#for sockets
import sys	#for exit
import threading
import time


def ip_checksum(data):  # Form the standard IP-suite checksum
	pos = len(data)
	if (pos & 1):  # If odd...
		pos -= 1
		sum = ord(data[pos])  # Prime the sum with the odd end byte
	else:
		sum = 0

	#Main code: loop to calculate the checksum
	while pos > 0:
		pos -= 2
		sum += (ord(data[pos + 1]) << 8) + ord(data[pos])

	sum = (sum >> 16) + (sum & 0xffff)
	sum += (sum >> 16)

	result = (~ sum) & 0xffff  # Keep lower 16 bits
	result = result >> 8 | ((result & 0xff) << 8)  # Swap bytes
	return chr(result / 256) + chr(result % 256)

# create dgram udp socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print 'Failed to create socket'
	sys.exit()

host = 'localhost';
port = 8888;
#sequence will change later
sequence = 0;
msg = ['hello0','hello1', 'hello2', 'hello3']

#handle problem if didn't get response
def thread_function(rmsg):
	print 'didn"t get mesage, resend mesage'
	
	print 'resend ack' + str(rmsg[:1])
	
	s.sendto(rmsg, (host, port))






while(1) :
	#msg = raw_input('Enter message to send : ')

	try :
		#Set the whole string

		#initialize list
		checksum_list = []
		send_socket_list = []
		print 'start?'
		y = input()
		##create sockets
		for i in msg:
			#print(i)
			checksum = ip_checksum(i)
			checksum_list.append(checksum)
			send_socket_list.append(str(sequence) + str(checksum) + i)
			if (sequence ==0):
				sequence = 1
			else:
				sequence = 0

			#print'sending ack' + str(sequence)
			#s.sendto(send_socket, (host, port))
			#x = threading.Timer(1.0, thread_function,[send_socket])
		
		##send socket with windows size of 2
		j = 0
		print'sending package0'
		s.sendto(send_socket_list[0], (host, port))
		x = threading.Timer(10.0, thread_function,[send_socket_list[0]])
		x.start()
		time.sleep(1)
		d = s.recvfrom(1024)
		
		reply = d[0]
		addr = d[1]
		
		#if if the message successfully received, cancel timer
		if( send_socket_list[0][:1] == str(reply[:1])):
			print('got the message back')
			print 'message echo: ' + reply[1:]
			x.cancel()
		else: 	# in this case if it is delayed ACK, simply ignore the package
				# this wouldn't cause chaos because sender is the one who decide if ACK has problem
			print("received duplicate message")
			print("message ignored")

		y = []
		for i in range(1,4):
			print'sending package',i
			s.sendto(send_socket_list[i], (host, port))
			temp = i
			y.append(threading.Timer(10.0, thread_function,[send_socket_list[temp]]))
			y[i-1].start()
			#time.sleep(1)

			

		for i in range(1,4):
			d = s.recvfrom(1024)
			reply = d[0]
			addr = d[1]
			
			#if if the message successfully received, cancel timer
			if( send_socket_list[i][:1] == str(reply[:1])):
				print('got the message back')
				print 'message echo: ' + reply[1:]
				y[i-1].cancel()
			else: 	# in this case if it is delayed ACK, simply ignore the package
					# this wouldn't cause chaos because sender is the one who decide if ACK has problem
				print("received duplicate message")
				print("message ignored")	



		#checksum = ip_checksum(msg)

		#concatenate same type: strings
		#send_socket = str(sequence) + str(checksum) + msg

		#print'sending ack' + str(sequence)
		#s.sendto(send_socket, (host, port))
		
		#handle timeout, only wait 1 second
	#	x = threading.Timer(1.0, thread_function,[send_socket])
		
		

		# receive data from client (data, addr)
		'''
		d = s.recvfrom(1024)
		
		reply = d[0]
		addr = d[1]
		
		#if if the message successfully received, cancel timer
		if( str(sequence) == str(reply[:1])):
			print('got the message')
			print (reply)
			x.cancel()
		else: 	# in this case if it is delayed ACK, simply ignore the package
				# this wouldn't cause chaos because sender is the one who decide if ACK has problem
			print("received duplicate message")
			print("message ignored")


			#print (sequence)
			#print(reply[:1])
		'''
		'''
		if (sequence ==0):
			sequence = 1
		else:
			sequence = 0
		'''
		time.sleep(2)

		print' '
		'''
		print 'Server reply : '
		print 'ack ' + reply[:1] 
		print 'message echo: ' + reply[1:]
		'''
		print '============================================='


	except socket.error, msg:
		print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()