
class PlayerInventory():
    def __init__(self):
        self.playerCollection = {}
        
    def updateInventoryCardCount(self, line):
        cardLine = line.split(':',maxsplit=1)
        cardId = cardLine[0].strip(' "')
        cardCount = cardLine[1].strip().strip(',')
        self.playerCollection[cardId] = cardCount
        
    def updatePlayerInventory(self, infile):
        line = infile.readline()
        if "{" in line:
            bracketCounter = 1
            while bracketCounter > 0:
                line = infile.readline()
                if "{" in line:
                    bracketCounter = bracketCounter+1
                if "}" in line:
                    bracketCounter = bracketCounter-1
                if ":" in line:
                    self.updateInventoryCardCount(line)

    def getInventory(self):
        return self.playerCollection
