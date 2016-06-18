import sys
import socket, asyncore

import math
from decimal import *
getcontext().prec = 4

import pygame
import json
from pygame.locals import *
pygame.init()

#pygame stuff----------------------------------------------------------
#screenX, screenY = 600, 600
#Screen = pygame.display.set_mode((screenX, screenY))
#clock = pygame.time.Clock()
#font = pygame.font.SysFont('Calibri', 15)
#Black = pygame.Color(0,0,0)
#White = pygame.Color(255,255,255)


class player(object):
    def __init__(self, clientsocket, address):
        #fancy connection stuff
        self.s = clientsocket
        self.ip = address[0]
        self.port = address[1]
        #game stuff
        self.name = "Player"
        
    def myreceive(self):
        #Recieve quantity of words
        chunks = []
        bytes_recd = 0
        while bytes_recd < 4:
            chunk = self.s.recv(min(4 - bytes_recd, 2048))
            if chunk == '':
                print self.name + " has disconnected"
                break
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        MSGLEN = int(''.join(chunks))
        #recieve the words
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.s.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                print self.name + " has disconnected"
                break
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)

serverport = 7778

serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind((socket.gethostname(), serverport))
#become a server socket
serversocket.listen(5)

print "Starting Host"
running = True
while running:
    #accept connections
    print "Accepting connections"
    (clientsocket, address) = serversocket.accept()
    thisplayer = player(clientsocket, address)
    #do something with clientsocket
    print "Connected "+str(thisplayer.ip)+" on port "+str(thisplayer.port)
    print thisplayer.myreceive()
    
    
print "Done"