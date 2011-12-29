import socket

WOLLIST = '/etc/enigma2/wollist'

def getArpList():
	result = []
	arp = open('/proc/net/arp', 'r')
	arp.readline() # skip header line
	for a in arp:
		item = a.split()
		result.append((item[0], item[3])) # IP, MAC
	return result

# Convert "aa:bb:cc..." to binary
def macToBin(mac):
	return ''.join([chr(int(x,16)) for x in mac.split(':')])

def sendWOL(mac):
	binmac = macToBin(mac)
	packet = '\xff'*6 + binmac * 16
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto(packet, ('<broadcast>', 9))

def getWOLList():
	result = []
	for line in open(WOLLIST, 'r'):
		line = line.strip()
		if line and not line.startswith('#'):
			result.append(line)
	return result

def sendAllWOL():
	lines = getWOLList()
	for repeat in range(2):
		for mac in lines:
			try:
				sendWOL(mac)
			except Exception, ex:
				print "Failed to wake '%s':" % mac, ex

