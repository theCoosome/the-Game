def prints(stuff):
    print stuff

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
            input = raw_input("Provide: ")
            
class comms(object):
    def say(self, who, said):
        prints(who.name + ": " + said)
        
    def tell(self, teller, told, said):
        prints(teller.name + " told " + told.name + ": " + said)
comm = comms()
        
        
class player(object):
    def __init__(self, clientsocket, address, playername):
        #fancy connection stuff
        self.s = clientsocket
        self.ip = address[0]
        self.port = address[1]
        #game stuff
        self.name = playername
        
        
players = []
players.append(player("socket", ("localhost", 7778), raw_input("name: ")))
players.append(player("socket", ("anotherone", 7778), "Siv"))
players.append(player("socket", ("itsdatboi", 7778), "Ben"))

thisplayer = players[0]


while True:
    word = raw_input(":")
    if " " in word:
        #More than one word----------------------------
        thewords = getwords(word, 2)
        
        if thewords[0].lower() == "tell":
            notsaid = True
            thesewords = getwords(thewords[1], 2)
            for i in players:
                if i.name.lower() == thesewords[0].lower():
                    notsaid = False
                    comm.tell(thisplayer, i, thesewords[1])
            if notsaid:
                prints("player "+thesewords[0]+" not found.")
            
        elif thewords[0].lower() == "say":
            comm.say(thisplayer, thewords[1])
            
        elif thewords[0].lower() == "list":
            if thewords[1].lower() == "players":
                toprint = "\nAll players:"
                for i in players:
                    toprint += "\n"+i.name
                prints(toprint+"\n")
            else:
                prints("Unable to list "+thewords[1]+". Listable:\n-players")
        else:
            comm.say(thisplayer, thewords[1])
        
    else:
        #Only one word---------------------------------
        if word == "help":
            prints("haha not happening yet")
        else:
            comm.say(thisplayer, word)



























