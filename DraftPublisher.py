from CardMap import CardMap
import json
import sys
import DraftFile

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow

class DraftPublisher(QWidget):
    
    def __init__(self):
        super().__init__()
        self.cardMap = CardMap()

    def getCardInfo(self, cardId):
        for card in self.cardMap.getMap():
            if cardId == card['ID']:
                return card
        return {"ID":"-1", "name":"Card Not Found"}

    def getCardName(self, cardId):
        return self.getCardInfo(cardId)['name']

    def pickExistsInData(self, draftData, pack, pick):
        return 'p'+str(pack)+'p'+str(pick)+'pick' in draftData
    
    def buildPickString(self, draftData, pack, pick):
        cardString=""
        pickString = "====================p"+str(pack+1)+'p'+str(pick+1)+"===============================\n"
        pickedCardId = draftData['p'+str(pack)+'p'+str(pick)+'pick']['params']['cardId']
        pickData = draftData['p'+str(pack)+'p'+str(pick)]['draftPack']
        if pickData == None and draftData['p'+str(pack)+'p'+str(pick)]['draftStatus'] == 'Draft.Complete':
            cardString = self.getCardName(pickedCardId)
            pickString = pickString + cardString + '  <==\n'
        else:
            for card in pickData:
                cardString = self.getCardName(card)
                if card == pickedCardId:
                    cardString = cardString + '  <=='
                cardString = cardString +'\n'
                pickString = pickString + cardString
        pickString = pickString +"=======================================================\n"
        return pickString
            
    def buildDeckString(self, deckData):
        deckString="========================== Maindeck ================================\n"
        for card in deckData['mainDeck']:
            if card['quantity'] > 0:
                cardString = self.getCardName(card['id'])
                cardString = str(card['quantity']) + "x " + cardString +'\n'
                deckString = deckString + cardString

        deckString=deckString + "\n========================== Sideboard ================================\n"
        for card in deckData['sideboard']:
            if card['quantity'] > 0:
                cardString = self.getCardName(card['id'])
                cardString = str(card['quantity']) + "x " + cardString +'\n'
                deckString = deckString + cardString
                
        return deckString

    def exportDraftLog(self, infile, outfile):
        draftData = DraftFile.loadDraftFile(infile)
        with open(outfile, 'w+') as of:
            for pack in range(3):
                for pick in range(15):
                    if self.pickExistsInData(draftData, pack, pick):
                        pickString = self.buildPickString(draftData, pack, pick)
                        of.write(pickString)
            deckString = self.buildDeckString(draftData['deck'])
            of.write(deckString)
        
    def exportFile(self, draftLogFile = None, outfile = None):
        if draftLogFile:
            infilename = draftLogFile
        else:
            infilename = QFileDialog.getOpenFileName(self, "Select a Draft Log to Export", directory='DraftLogs', filter="DraftLog Files (*.json)")[0]
        if outfile:
            outfilename = outfile
        else:
            outfilename = QFileDialog.getSaveFileName(self, "Name your Draft Export", directory='DraftLogs', filter="Draft Export Text File (*.txt)")[0]
        self.exportDraftLog(infilename,outfilename)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    publisher = DraftPublisher()
    publisher.exportFile()
    sys.exit(app.exec_())
