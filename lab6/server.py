import socket
import sys
import time


# Code taken from http://codewiki.wikispaces.com/ip_checksum.py.


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

def sndpkt(data, checksum):
	d = ip_checksum(data)
	return d



HOST = ''	# Symbolic name meaning all available interfaces
PORT = 8888	# Arbitrary non-privileged port

# Datagram (udp) socket
try :
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Socket created'
except socket.error, msg :
	print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()


# Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
	
print 'Socket bind complete'


#now keep talking with the client
while 1:
	# receive data from client (data, addr)
	d = s.recvfrom(1024)
	data = d[0]
	addr = d[1]
	
	if not data: 
		break
	# sequence + checksum + data = data received

	sequence = data[:1]

	received_cehcksum = ip_checksum(data[3:])
	checksum = data[1:3]
	
	if (received_cehcksum == checksum):
		print('checksum match')
	else:
		print('checksum doesn"t match')
		time.sleep(1)
		continue

	if sequence == '0':
		reply = '0'
		print('got ack0, now sending ack0')
	elif sequence == '1':
		reply = '1'
		print('got ack1, now sending ack1')


	#sndpkt(data)
	#print('reply is ', reply)
	reply = reply + data[3:]
	#print('reply is ', reply)
	#time.sleep(2.2)
	s.sendto(reply , addr)
	print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data[3:]
	print'================================================'
	#d1 = ip_checksum()
	


s.close()