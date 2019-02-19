import json

class CardMap():
    def __init__(self):
        self.cardMapJson = self.loadCardMap()
        
    def loadCardMap(self):
        with open("cards-parsed.json") as f:
            cardMapJson = json.load(f)
        return cardMapJson

    def getMap(self):
        return self.cardMapJson
    
    def getCardInfo(self, cardId):
        for card in self.cardMapJson:
            if cardId == card['ID']:
                return card
        return {"ID":"-1", "name":"Card Not Found"}

    def getCardInfoByName(self, cardName):
        for card in self.cardMapJson:
            if cardName == card['name']:
                return card
        return {"ID":"-1", "name":"Card Not Found"}

    def getCardName(self, cardId):
        return self.getCardInfo(cardId)['name']

    def cardSortKey(card):
        raritymap = { "mythic":"0", "rare":"1", "uncommon":"2", "common":"3"}
        return raritymap[card['rarity']]+card['ID']
