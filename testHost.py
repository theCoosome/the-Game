print "Starting Host"
import sys
import socket, asyncore

import math
from decimal import *
getcontext().prec = 4

#import pygame
#import json
#from pygame.locals import *
#pygame.init()

#pygame stuff----------------------------------------------------------
#screenX, screenY = 600, 600
#Screen = pygame.display.set_mode((screenX, screenY))
#clock = pygame.time.Clock()
#font = pygame.font.SysFont('Calibri', 15)
#Black = pygame.Color(0,0,0)
#White = pygame.Color(255,255,255)

def cuttofour(number):
    number = str(number)
    leng = len(number)
    if leng > 4:
        print "Packet too long. Cutting " + str(int(number)-int(number[:4])) + " digits"
        number = number[:4]
    if leng < 4:
        rand = 4-leng
        print "splicing " + str(rand) + " leading zeros"
        for i in range(rand):
            number = "0"+number
    return number
    

class player(object):
    def __init__(self, clientsocket, address):
        #fancy connection stuff
        self.s = clientsocket
        self.ip = address[0]
        self.port = address[1]
        #game stuff
        self.name = "Player"
        self.connected = True
        
    def myreceive(self):
        #Recieve quantity of words
        chunks = []
        bytes_recd = 0
        while bytes_recd < 4:
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
            while bytes_recd < MSGLEN:
                chunk = self.s.recv(min(MSGLEN - bytes_recd, 2048))
                if chunk == '':
                    print self.name + " has disconnected"
                    self.connected = False
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
            return ''.join(chunks)
        
        
    def sendinfo(self, typewords):
        #send size of packet
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

serverport = 7778

serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind((socket.gethostname(), serverport))
#become a server socket
serversocket.listen(5)


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

running = True
while running:
    for i in players:
        print i.myreceive()
        #i.sendinfo("Confirming hl3")
        if i.connected == False:
            players.remove(i)
    
    if len(players) <= 0:
        running = False
print "Done"