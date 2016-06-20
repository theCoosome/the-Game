import sys
import socket

import math
from decimal import *
getcontext().prec = 4

import pygame
import json
from pygame.locals import *
pygame.init()

screenX, screenY = 600, 600
clock = pygame.time.Clock()
font = pygame.font.SysFont('Calibri', 15)
Black = pygame.Color(0,0,0)
White = pygame.Color(255,255,255)
typewords = ""
capital = False

serverip = "75.175.26.183"
serverport = 7778
#serverip = "192.168.1.47"




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

def sendinfo(typewords):
    global s
    #send size of packet
    msg = cuttofour(len(typewords))
    totalsent = 0
    while totalsent < 4:
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
            break
        totalsent = totalsent + sent
    #send packet
    totalsent = 0
    while totalsent < int(msg):
        sent = s.send(typewords[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
            break
        totalsent = totalsent + sent
        
def myreceive():
    #Recieve quantity of words
    global s
    connected = True
    chunks = []
    bytes_recd = 0
    while bytes_recd < 4 and connected:
        chunk = s.recv(min(4 - bytes_recd, 2048))
        if chunk == '':
            print "Server has disconnected"
            connected = False
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    if connected:
        MSGLEN = int(''.join(chunks))
        #recieve the words
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN and connected:
            chunk = s.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                print "Server has disconnected"
                connected = False
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)
        
        
        
s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

s.connect((serverip, serverport))
print "Connected"
name = raw_input("Name:  ")
sendinfo(name)
print "Waiting for server to start..."
print myreceive()
'''
#bind the socket to a public host,
# and a well-known port
serversocket.bind((socket.gethostname(), serverport))
#become a server socket
serversocket.listen(5)'''

def typing(thisevent, eventwanted, typing):
    if event.key == eventwanted:
        global capital
        global typewords
        if capital:
            typewords += typing.upper()
        else:
            typewords += typing.lower()


Screen = pygame.display.set_mode((screenX, screenY))
running = True
while running:
    Screen.fill(White)
    tosend = "$"
    #Get external (server) input
    
    dialog = font.render("The Game Client", True, Black)
    Screen.blit(dialog, [0,0])
    dialog = font.render("Connected as: "+name, True, Black)
    Screen.blit(dialog, [0,20])
    dialog = font.render(typewords, True, Black)
    Screen.blit(dialog, [0,100])
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            #typing
            if event.key == K_SPACE:
                typewords += " "
            typing(event, K_q, "q")
            typing(event, K_w, "w")
            typing(event, K_e, "e")
            typing(event, K_r, "r")
            typing(event, K_t, "t")
            typing(event, K_y, "y")
            typing(event, K_u, "u")
            typing(event, K_i, "i")
            typing(event, K_o, "o")
            typing(event, K_p, "p")
            typing(event, K_a, "a")
            typing(event, K_s, "s")
            typing(event, K_d, "d")
            typing(event, K_f, "f")
            typing(event, K_g, "g")
            typing(event, K_h, "h")
            typing(event, K_j, "j")
            typing(event, K_k, "k")
            typing(event, K_l, "l")
            typing(event, K_z, "z")
            typing(event, K_x, "x")
            typing(event, K_c, "c")
            typing(event, K_v, "v")
            typing(event, K_b, "b")
            typing(event, K_n, "n")
            typing(event, K_m, "m")
            if event.key == K_1:
                typewords += "1"
            if event.key == K_2:
                typewords += "2"
            if event.key == K_3:
                typewords += "3"
            if event.key == K_4:
                typewords += "4"
            if event.key == K_5:
                typewords += "5"
            if event.key == K_6:
                typewords += "6"
            if event.key == K_7:
                typewords += "7"
            if event.key == K_8:
                typewords += "8"
            if event.key == K_9:
                typewords += "9"
            if event.key == K_0:
                typewords += "0"
            if event.key == K_PERIOD:
                typewords += "."
            if event.key == K_COMMA:
                typewords += ","
            if event.key == K_SLASH and capital:
                typewords += "?"
            
            #more advanced
            if event.key == K_BACKSPACE and len(typewords) > 0:
                typewords = typewords[:len(typewords)-1]
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                capital = True
            if event.key == K_RETURN and len(typewords) > 0:
                #--Send words-------------------------------------------------------------------------------------------------
                tosend = typewords
                #print "Sent "+typewords
                typewords = ""
        if event.type == pygame.KEYUP:
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                capital = False
    
    sendinfo(tosend)
    recieved = myreceive()
    if recieved != "$":
        print recieved
    pygame.display.update()
    clock.tick(40)
print "Done"