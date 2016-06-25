print "Starting Host"
import sys
import socket, asyncore

import math
from decimal import *
getcontext().prec = 4

#Send $ to pass, send % to start new line

def cuttofour(number):
    number = str(number)
    leng = len(number)
    if leng > 4:
        print "Packet too long. Cutting " + str(int(number)-int(number[:4])) + " digits"
        number = number[:4]
    if leng < 4:
        rand = 4-leng
        #print "splicing " + str(rand) + " leading zeros"
        for i in range(rand):
            number = "0"+number
    return number
    

class player(object):
    def __init__(self, clientsocket, address):
        #fancy connection stuff
        self.s = clientsocket
        self.ip = address[0]
        self.port = address[1]
        self.connected = True
        self.tosend = ""
        #game stuff
        self.catag = "Human"
        self.name = "Player"
        self.hp = 100
        self.bsmaxhp = 100
        self.maxhp = 100
        self.bsatk = 8
        self.atk = 8
        self.bsdef = 0
        self.dfn = 0
        self.bsddev = 10
        self.ddev = 10
        self.bshealval = 1
        self.healval = 1
        self.hdev = 3
        self.bsagil = [18, 100]
        self.agil = [15, 100]
        self.lvl = 1
        self.sane = 8
        self.trueSane = 0
        self.minions = []
        self.minionTree = []
        
    def myreceive(self):
        #Recieve quantity of words
        chunks = []
        bytes_recd = 0
        while bytes_recd < 4 and self.connected:
            chunk = self.s.recv(min(4 - bytes_recd, 2048))
            if chunk == '':
                print self.name + " has disconnected"
                self.connected = False
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        if self.connected:
            MSGLEN = int(''.join(chunks))
            #recieve the words
            chunks = []
            bytes_recd = 0
            while bytes_recd < MSGLEN and self.connected:
                chunk = self.s.recv(min(MSGLEN - bytes_recd, 2048))
                if chunk == '':
                    print self.name + " has disconnected"
                    self.connected = False
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
            return ''.join(chunks)
        
        
    def sendinfo(self, typewords):
        #send size of packet
        try:
            msg = cuttofour(len(typewords))
            totalsent = 0
            while totalsent < 4:
                sent = self.s.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                    break
                totalsent = totalsent + sent
            #send packet
            totalsent = 0
            while totalsent < int(msg):
                sent = self.s.send(typewords[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                    break
                totalsent = totalsent + sent
        except socket.error:
            self.connected = False

serverport = 7778

serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind((socket.gethostname(), serverport))
#become a server socket
serversocket.listen(5)


connecting = raw_input("Expected turnout:   ")


print socket.gethostbyname(socket.gethostname())
players = []
for i in range(int(connecting)):
    print "Accepting connections"
    #accept connections
    (clientsocket, address) = serversocket.accept()
    thisplayer = player(clientsocket, address)
    print "Connected "+str(thisplayer.ip)+" on port "+str(thisplayer.port)
    thisplayer.name = thisplayer.myreceive()
    players.append(thisplayer)
    print "Player "+str(len(players))+" now using alias " + players[len(players)-1].name
print "Connected "+str(len(players))+" players total."

for i in players:
    i.sendinfo("Connected "+str(len(players))+" players total")

running = True
while running:
    tosend = ""
    #Recieve from all players
    for i in players:
        i.tosend = ""
        recieved = i.myreceive()
        if recieved != "$":
            print recieved
            #Run interpreter here-----------------------------------------------------------------------
            tosend += i.name+":  "+recieved
            #add to tosend
        if i.connected == False:
            players.remove(i)
    
    #Send to all players
    for i in players:
        i.tosend = tosend+"\n"+i.tosend
        if tosend == "\n":
            tosend = "$"
        i.sendinfo(i.tosend)
    
    if len(players) <= 0:
        running = False
print "Done"
