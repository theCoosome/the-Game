print "Starting Host"
import sys
import socket, asyncore

import math
from decimal import *
getcontext().prec = 4

#import pygame
#pygame.init()
#clock = pygame.time.Clock()

#Send $ to pass, % to disconnect

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
        self.name = "Player"
        
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
    
def addtosend(thing, stuff):
    if thing == "$" or thing == "":
        thing = stuff
    else:
        thing += "\n"+stuff
    return thing
    
def getwords(input, quant):
    retreving = True
    words = []
    while retreving:
        word = ""
        getting = True
        for i in input:
            if i == " " and getting:
                words.append(word)
                word = ""
                if len(words)+1 >= quant:
                    getting = False
            else:
                word = word+i
        words.append(word)
        if len(words) == quant:
            return words
            retreving = False
        else:
            prints("Missing "+str(quant-len(words))+" values")
            input = raw_input("Provide: ")#NEED FIX----------------------------------------------
    
class comms(object):
    def say(self, who, said):
        global tosend
        tosend = addtosend(tosend, who.name + ": " + said)
        
        
comm = comms()

def Interpret(word, sayer):
    global players
    global comm
    global tosend
    if " " in word:
        #More than one word----------------------------
        thewords = getwords(word, 2)
        
        if thewords[0].lower() == "tell":
            notsaid = True
            thesewords = getwords(thewords[1], 2)
            for i in players:
                if i.name.lower() == thesewords[0].lower():
                    notsaid = False
                    print sayer.name + " told " + i.name + ": " + thesewords[1]
                    i.tosend = addtosend(i.tosend, sayer.name+" --> you: "+thesewords[1])
                    sayer.tosend = addtosend(sayer.tosend, "you --> "+i.name+": "+thesewords[1])
            if notsaid:
                sayer.tosend = addtosend(sayer.tosend, "player "+thesewords[0]+" not found.")
            
        elif thewords[0].lower() == "say":
            comm.say(sayer, thewords[1])
            
        elif thewords[0].lower() == "list":
            if thewords[1].lower() == "players":
                sayer.tosend = addtosend(sayer.tosend, "\nAll players:")
                for i in players:
                    sayer.tosend = addtosend(sayer.tosend, i.name)
            else:
                sayer.tosend = addtosend(sayer.tosend, "Unable to list "+thewords[1]+". Listable:\n-players")
        
        else:
            comm.say(sayer, word)
        
    else:
        #Only one word---------------------------------
        if word == "help":
            sayer.tosend = addtosend(sayer.tosend, "haha not happening yet")
        else:
            comm.say(sayer, word)

serverport = 7778

#Get info from previous games here---------------------------------------------------------------------------------------------------

serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind((socket.gethostname(), serverport))
#become a server socket
serversocket.listen(5)

    
#CONNECTING PLAYERS
connecting = raw_input("Expected turnout:   ")
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
        i.tosend = "$"
        recieved = i.myreceive()
        if recieved != "$":
            if recieved == "%":
                i.connected = False
            else:
                print i.name + recieved
                Interpret(recieved, i)
        if i.connected == False:
            tosend = addtosend(tosend, i.name+" has disconnected")
            
            players.remove(i)
    
    #Send to all players
    for i in players:
        if tosend != "":
            i.tosend = addtosend(i.tosend, tosend)
        i.sendinfo(i.tosend)
    
    if len(players) <= 0:
        running = False
    #clock.tick(3)