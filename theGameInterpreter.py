def prints(stuff):
    print stuff
    
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
        self.bsheal = 1
        self.heal = 1
        self.hdev = 3
        self.bsagil = 18
        self.agil = [18, 100]
        self.lvl = 1
        self.bssane = 8
        self.sane = 8
        self.trueSane = 0
        #other
        self.minions = []
        self.minionTree = []
        self.inventory = []
        self.equipped = []
        #equip regions, how many things are there: head, torso, hands, legs, feet
        self.equipRegions = [0, 1, 0, 2, 2]
        self.maxRegions = [3, 3, 2, 3, 2]
        
    #takes string of item name
    def equip(self, word):
        failedName, successEquip = True, True
        for i in self.inventory:
            if word.lower() == i.name.lower():
                failedName = False
                for x in range(5):
                    if self.equipRegions[x]+i.equipRegions[x] > self.maxRegions[x]
                        successEquip = False
                if successEquip:
                    equipped.append(i)
                    inventory.remove(i)
                    self.reStat()
                    tosend = addtosend(tosend, self.name+" equipped "+word)
                else:
                    self.tosend = addtosend(self.tosend, "Not enough room to equip "+word)
                break
        if failedName:
            self.tosend = addtosend(self.tosend, "No item in inventory called "+word)
        
    def reStat(self):
        #recalculate all stats based on items and anything else
        atkmod, ddevmod, dfnmod, agilmod, hpmod, healmod, sanemod = 0, 0, 0, 0, 0, 0, 0
        for i in self.equipped:
            atkmod, ddevmod, dfnmod, agilmod, hpmod, healmod, sanemod += i.atkmod, i.ddevmod, i.dfnmod, i.agilmod, i.hpmod, i.healmod, i.sanemod
        self.atk = self.bsatk+atkmod
        self.ddev = self.bsddev+ddevmod
        self.dfn = self.bsdfn+dfnmod
        self.agil = [self.bsagil+agilmod, 100]
        self.maxhp = self.bsmaxhp+hpmod
        self.heal = self.bsheal+healmod
        self.sane = self.bssane+sanemod

    
players = []
players.append(player("socket", ("localhost", 7778), "Coo"))
players.append(player("socket", ("anotherone", 7778), "Siv"))
players.append(player("socket", ("itsdatboi", 7778), "Ben"))

itemframes = []
itemframes.append([6, -1, 1, -1, 0, 0, [0, 0, ]])
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
        self.equipRegions = eq

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



























