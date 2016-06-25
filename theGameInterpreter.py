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
        self.status = "Doing quite well, actually"
        #stats
        self.hp = 100
        self.bsmaxhp = 100
        self.maxhp = 100
        #self.mana = 15
        #self.bsmaxmana = 15  #oh god this is gonna be painful
        #self.maxmana = 15
        self.bsatk = 8
        self.atk = 8
        self.bsdfn = 0
        self.dfn = 0
        self.bsddev = 10
        self.ddev = 10
        self.bshealval = 1
        self.healval = 1
        self.hdev = 3
        self.bsagil = [18, 100]
        self.agil = [15, 100]
        self.lvl = 1
        self.bssane = 8
        self.sane = 8
        self.trueSane = 0
        #other
        self.minions = []
        self.minionTree = []
        self.inventory = []
        self.equipped = []
        #equip regions, if something is there
        self.Rhead = False
        self.Rtorso = False
        self.RLhand = False
        self.RRhand = False
        self.Rlegs = False
        self.Rfeet = False
        
    def equip(self, item):
        pass
        
    def reStat(self):
        #recalculate all stats based on items and anything else
        for i in self.equipped:
            pass

    
players = []
players.append(player("socket", ("localhost", 7778), "Coo"))
players.append(player("socket", ("anotherone", 7778), "Siv"))
players.append(player("socket", ("itsdatboi", 7778), "Ben"))


class Item(object):
    def __init__(self, atkmod, ddevmod, dfnmod, agilmod, hpmod, healmod, sanemod, eq, catag, name):
        #Descriptive
        self.catag = catag
        self.name = name
        self.status = "Brand spankin' new"
        #stats
        #self.mana = 15
        #self.manamod = 15  #oh god this is gonna be painful
        self.atkmod = atkmod
        self.ddevmod = ddevmod
        self.dfnmod = dfnmod
        self.agilmod = agilmod
        self.hpmod = hpmod
        self.healmod = healmod
        self.sanemod = sanemod
        #equip regions, if it takes it up
        self.Rhead = eq[0]
        self.Rtorso = eq[1]
        self.RLhand = eq[2]
        self.RRhand = eq[3]
        self.Rlegs = eq[4]
        self.Rfeet = eq[5]

entityframes = []
class entity(object):
    def __init__(self, ):
        self.catag = "Human"
        self.name = "Player"
        self.hp = hp
        self.bsmaxhp = hp
        self.maxhp = maxhp
        self.bsatk = atk
        self.atk = atk
        self.bsdfn = dfn
        self.dfn = dfn
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

entities = []

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
			prints("Current Commands:")
			prints("say <message>")
			prints("say something to everyone")
			prints("tell <player> <message>")
			prints("tell a player a message")
			
        else:
            comm.say(thisplayer, word)



























