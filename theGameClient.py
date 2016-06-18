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
Screen = pygame.display.set_mode((screenX, screenY))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Calibri', 15)
Black = pygame.Color(0,0,0)
White = pygame.Color(255,255,255)
typewords = ""

serverip = "75.175.26.183"
serverport = 7778
#serverip = "10.0.1.18"

s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

s.connect((serverip, serverport))
print "Connected"


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
        
running = True
while running:
    Screen.fill(Black)
    
    #Get external (server) input
    
    dialog = font.render("The Game  Client", True, White)
    Screen.blit(dialog, [0,0])
    dialog = font.render(typewords, True, White)
    Screen.blit(dialog, [0,100])
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            #typing
            if event.key == K_SPACE:
                typewords += " "
            if event.key == K_q:
                typewords += "q"
            if event.key == K_w:
                typewords += "w"
            if event.key == K_e:
                typewords += "e"
            
            #more advanced
            if event.key == K_BACKSPACE and len(typewords) > 0:
                typewords = typewords[:len(typewords)-1]
            if event.key == K_RETURN and len(typewords) > 0:
                #--Send words-------------------------------------------------------------------------------------------------
                sendinfo(typewords)
                print "Sent "+typewords
                typewords = ""
    
    pygame.display.update()
    clock.tick(60)
print "Done"