def prints(stuff):
    print stuff
    
def addtosend(thing, stuff):
    if thing == "$" or thing == "":
        thing = stuff
    else:
        thing += "\n"+stuff
    return thing

def getwords(input, quant):
    retreving, quotes = True, False
    words = []
    while retreving:
        word = ""
        getting = True
        for i in input:
            if i == "'" or i == '"':
                if quotes:
                    quotes = False
                else:
                    quotes = True
            if i == " " and getting and not quotes:
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
            #$ signifies error, ammount of words retrieved, error message
            return ["$", len(words), "Missing "+str(quant-len(words))+" values"]
            
            
            

class comms(object):
    def say(self, who, said):
        global tosend
        tosend = addtosend(tosend, who.name + ": " + said)
    
    def makeitem(self, stats, id="$"):
        if id == "$":
            return Item(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6], stats[7], stats[8], stats[9])
        else:
            return Item(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6], stats[7], stats[8], stats[9], id)
        
comm = comms()
            
            
class Item(object):
    def __init__(self, atkmod, ddevmod, dfnmod, agilmod, hpmod, healmod, sanemod, eq, catag, name, title="$"):
        #Descriptive
        self.catag = catag
        self.name = name
        self.status = "Brand spankin' new"
        if title == "$":
            self.title = name
        else:
            self.title = title
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

itemframes, items = [], []
itemframes.append([0, 0, 1, 0, 0, -1, 1, [0, 1, 0, 0, 0], "Clothing", "Shirt"])
itemframes.append([0, 0, 0, 0, 0, 0, 1, [0, 1, 0, 0, 0], "Clothing", "Undies"])
itemframes.append([0, 0, 1, 0, 0, -1, 1, [0, 1, 0, 0, 0], "Clothing", "Pants"])
itemframes.append([0, -1, 0, 0, 0, 0, 1, [0, 0, 0, 0, 1], "Clothing", "Shoes"])
items.append(comm.makeitem(itemframes[0]))
items.append(comm.makeitem(itemframes[1]))
items.append(comm.makeitem(itemframes[2]))
items.append(comm.makeitem(itemframes[3]))


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
            if word.lower() == i.name.lower() or word.lower() == i.title.lower():
                failedName = False
                for x in range(5):
                    if self.equipRegions[x]+i.equipRegions[x] > self.maxRegions[x]:
                        successEquip = False
                if successEquip:
                    equipped.append(i)
                    inventory.remove(i)
                    self.reStat()
                    tosend = addtosend(tosend, self.name+" equipped "+i.title)
                else:
                    self.tosend = addtosend(self.tosend, "Not enough room to equip "+i.title)
                break
        if failedName:
            self.tosend = addtosend(self.tosend, "No item in inventory called "+word)
        
    def unequip(self, word):
        failedName, successEquip = True, True
        for i in self.equipped:
            if word.lower() == i.name.lower() or word.lower() == i.title.lower():
                failedName = False
                equipped.remove(i)
                inventory.append(i)
                tosend = addtosend(tosend, self.name+" unequipped "+i.title)
                break
        if failedName:
            self.tosend = addtosend(self.tosend, "No item called "+i.name+" equipped.")
                #--------------------------------------------------------------------------------------------------------------
        
    def reStat(self):
        #recalculate all stats based on items and anything else
        atkmod, ddevmod, dfnmod, agilmod, hpmod, healmod, sanemod = 0, 0, 0, 0, 0, 0, 0
        self.equipRegions = [0, 0, 0, 0, 0]
        for i in self.equipped:
            atkmod += i.atkmod
            ddevmod += i.ddevmod
            dfnmod += i.dfnmod
            agilmod += i.agilmod
            hpmod += i.hpmod
            healmod += i.healmod
            sanemod += i.sanemod
            self.equipRegions += i.eq
        self.atk = self.bsatk+atkmod
        self.ddev = self.bsddev+ddevmod
        self.dfn = self.bsdfn+dfnmod
        self.agil = [self.bsagil+agilmod, 100]
        self.maxhp = self.bsmaxhp+hpmod
        self.heal = self.bsheal+healmod
        self.sane = self.bssane+sanemod

    
players = []
players.append(player("socket", ("localhost", 7778)))
players.append(player("socket", ("anotherone", 7778)))
players.append(player("socket", ("itsdatboi", 7778)))
players[0].name = "Coo"
players[1].name = "Siv"
players[2].name = "Ben"

for i in players:
    i.equipped.append(items[0])
    i.equipped.append(items[1])
    i.equipped.append(items[2])
    i.equipped.append(items[3])

entityframes = []
class entity(object):
    def __init__(self, hp):
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

        
        

def Interpret(word, sayer):
    global players
    global comm
    global tosend
    if " " in word:
        #More than one word----------------------------
        #scaling thewords > thesewords > morewords
        thewords = getwords(word, 2)
        watdo = thewords[0].lower()
        if watdo == "tell":
            notsaid = True
            thesewords = getwords(thewords[1], 2)
            for i in players:
                if i.name.lower() == thesewords[0].lower():
                    notsaid = False
                    #print sayer.name + " told " + i.name + ": " + thesewords[1]
                    i.tosend = addtosend(i.tosend, sayer.name+" --> you: "+thesewords[1])
                    sayer.tosend = addtosend(sayer.tosend, "you --> "+i.name+": "+thesewords[1])
            if notsaid:
                sayer.tosend = addtosend(sayer.tosend, "player "+thesewords[0]+" not found.")
            
        elif watdo == "say":
            comm.say(sayer, thewords[1])
            
        #list <list> (catagory)
        elif watdo == "list":
            thesewords = getwords(thewords[1], 2)
            multiple = True
            if thesewords[0] == "$":
                thesewords = thewords[1].lower()
                multiple = False
                
            if thesewords == "players" or thesewords[0] == "players":
                if multiple:
                    #list players with a catagory
                    failed = True
                    for i in players:
                        if i.catag == thesewords[1]:
                            failed = False
                            sayer.tosend = addtosend(sayer.tosend, i.name)
                    if failed:
                        sayer.tosend = addtosend(sayer.tosend, "Failed to list players in catagory "+thesewords[1])
                            
                else:
                    #list all players
                    sayer.tosend = addtosend(sayer.tosend, "\nAll players:")
                    for i in players:
                        sayer.tosend = addtosend(sayer.tosend, i.name)
            
            elif thesewords == "frames" or thesewords[0] == "frames":
                if multiple:
                    failedType = True
                    if thesewords[1].lower() == "item":
                        failedType = False
                        global itemframes
                        #try to get catagory-----------------------------------------------------------------------------------------------------------------------
                        for i in itemframes:
                            sayer.tosend = addtosend(sayer.tosend, i[8]+" : "+i[9])
                        
                    elif thesewords[1].lower() == "entity":
                        failedType = False
                        global entityframes
                        for i in entityframes:
                            sayer.tosend = addtosend(sayer.tosend, "Catagory : name : title")#----------------------------------------------------Come back to when entities are ready
                        
                    if failedType:
                        sayer.tosend = addtosend(sayer.tosend, "Unable to list "+thesewords[1])
                #list all frames
                else:
                    global itemframes
                    global entityframes
                    sayer.tosend = addtosend(sayer.tosend, "\nItem frames:")
                    for i in itemframes:
                        sayer.tosend = addtosend(sayer.tosend, i[8]+" : "+i[9])
                    for i in entityframes:
                        sayer.tosend = addtosend(sayer.tosend, "Catagory : name : title")#--------------------------------------------------------Come back to when entities are ready
            else:
                sayer.tosend = addtosend(sayer.tosend, "Unable to list "+thewords[1]+". Listable:\n-players\n-frames")
                
        #see <object type> <catagory> <id> (stat)
        elif watdo == "see":
            failed = False
            thesewords = getwords(thewords[1], 4)
            if thesewords[0] == "$":
                #Run if stat is not specified
                thesewords = getwords(thewords[1], 3)
                if thesewords[0] == "$":
                    sayer.tosend = addtosend(sayer.tosend, thesewords[3])
                    failed = True
                if not failed:
                    sayer.tosend = addtosend(sayer.tosend, "These are not the stats you are looking for")
            else:
                sayer.tosend = addtosend(sayer.tosend, "Error 404: Lorem ipsum other castle, arrow to the knee set up us the bomb.")
                
        elif watdo == "new":
            thesewords = getwords(thewords[1], 2)
            if thesewords[0] == "$":
                sayer.tosend = addtosend(sayer.tosend, "You need to give stats to make something!")
            else:
                if thesewords[0].lower() == "item":
                    multiple = 11
                    morewords = getwords(thesewords[1], 11)
                    if morewords[0] == "$":
                        morewords = getwords(thesewords[1], 10)
                        multiple = 10
                        if morewords[0] == "$":
                            sayer.tosend = addtosend(sayer.tosend, "Only "+str(morewords[1])+" values given, "+morewords[2])
                            multiple = 0
                    if multiple == 11:
                        itemframes.append([morewords[0], morewords[1], morewords[2], morewords[3], morewords[4], morewords[5], morewords[6], morewords[7], morewords[8], morewords[9], morewords[10]])
                        sayer.tosend = addtosend(sayer.tosend, "Created item frame "+morewords[8]+" : "+morewords[9]+" : "+morewords[10])
                    elif multiple == 10:
                        itemframes.append([morewords[0], morewords[1], morewords[2], morewords[3], morewords[4], morewords[5], morewords[6], morewords[7], morewords[8], morewords[9]])
                        sayer.tosend = addtosend(sayer.tosend, "Created item frame "+morewords[8]+" : "+morewords[9])
        else:
            comm.say(sayer, word)
        
    else:
        #Only one word---------------------------------
        if word == "help":
            sayer.tosend = addtosend(sayer.tosend, "haha not happening yet")
        else:
            comm.say(sayer, word)



while True:
    tosend = ""
    thisplayer.tosend = "$"
    recieved = raw_input(":")
    Interpret(recieved, thisplayer)
    
    thisplayer.tosend = addtosend(thisplayer.tosend, tosend)
    print thisplayer.tosend






















