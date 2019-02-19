import sys
import json
from getpass import getuser

import DraftFile
from CardMap import CardMap
from UncommonPrintRun import UncommonPrintRun
from PlayerInventory import PlayerInventory

from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)

class MtgaDraftParser(QThread):
    draftPackUpdate = pyqtSignal(list, list)
    draftCompletion = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        username=getuser()
        self.logfilefullpath = "C:/Users/"+username+"/AppData/LocalLow/Wizards Of The Coast/MTGA/output_log.txt"
        self.playerInventory = PlayerInventory()
        self.cardMap = CardMap()
        self.uncommonPrintRun = UncommonPrintRun(self.cardMap)

    def run(self):
        with open(self.logfilefullpath) as f:
            print("Starting Parsing Log File")
            while True:
                c = f.readline()
                if not c == "":
                    self.dispatch_line_parsing(f,c)
                    
    def dispatch_line_parsing(self, infile,line):
        if "<==" in line[0:3]:
            if self.lineIsInventoryUpdate(line):
                self.playerInventory.updatePlayerInventory(infile)
            elif self.lineIsDraftStatus(line):
                self.processDraftStatus(infile)
            elif self.lineIsDraftCompletion(line):
                self.processDraftCompletion(infile)
            elif self.lineIsDeckSubmission(line):
                self.processDeckSubmission(infile)
        elif "==>" in line[0:3]:
            if self.lineIsDraftPick(line):
                self.processDraftPick(infile)

    def lineIsInventoryUpdate(self, line):
        return "<== PlayerInventory.GetPlayerCards" in line    

    def lineIsDraftStatus(self, line):
        return "<== Draft.DraftStatus" in line or "<== Draft.MakePick" in line

    def lineIsDraftPick(self, line):
        return "==> Draft.MakePick" in line

    def lineIsDeckSubmission(self, line):
        return "<== Event.DeckSubmit" in line

    def lineIsDraftCompletion(self, line):
        return "<== Event.CompleteDraft" in line

    def readStatusObject(self, infile):
        line = infile.readline()
        statusObjString = ""
        if "{" in line:
            statusObjString = line
            bracketCounter = 1
            while bracketCounter > 0:
                line = infile.readline()
                if "{" in line:
                    bracketCounter = bracketCounter+1
                if "}" in line:
                    bracketCounter = bracketCounter-1
                statusObjString = statusObjString + line
        return statusObjString
    
    def processDraftStatus(self, infile):
        draftStatusObjString = self.readStatusObject(infile)
        draftStatusObj = json.loads(draftStatusObjString)
        DraftFile.updateDraftFile(draftStatusObj)
        self.printMatchingCardCounts(draftStatusObj)

    def processDraftPick(self, infile):
        draftPickObjString = self.readStatusObject(infile)
        draftPickObj = json.loads(draftPickObjString)
        filename=DraftFile.getIncompleteDraftFilename(draftPickObj['params'])
        draftData = DraftFile.loadDraftFile(filename)
        draftData['p'+str(draftPickObj['params']['packNumber'])+'p'+str(draftPickObj['params']['pickNumber']+'pick')] = draftPickObj
        DraftFile.writeDraftFile(filename, draftData)

    def processDraftCompletion(self, infile):
        draftCompletionStatusObjString = self.readStatusObject(infile)
        draftCompletionStatusObj = json.loads(draftCompletionStatusObjString)
        finalizedFilename = DraftFile.finalizeDraft(draftCompletionStatusObj)
        self.draftCompletion.emit(finalizedFilename)

    def processDeckSubmission(self, infile):
        deckSubmissionObj = json.loads(self.readStatusObject(infile))
        if 'Draft' in deckSubmissionObj['InternalEventName']:
            draftRecordFilename = DraftFile.updateDraftDeck(deckSubmissionObj)
            self.draftCompletion.emit(draftRecordFilename)
        
    def printMatchingCardCounts(self, statusObj):
        if 'Draft.Complete' == statusObj['draftStatus']:
            return
        
        print("")
        print("=======================================================================")
        draftPack = []
        for cardId in statusObj['draftPack']:
            card = self.cardMap.getCardInfo(cardId)
            draftPack.append(card)

        draftPack.sort(key=CardMap.cardSortKey)
        uncommons = []
        for card in draftPack:
            if card['ID'] not in self.playerInventory.getInventory():
                card['owned'] = '0'
            else:
                card['owned'] = self.playerInventory.getInventory()[card['ID']]
            print("Card "+card['name']+" count: "+card['owned'])
            if card['rarity'] == 'uncommon':
                uncommons.append(card)

        setCode = statusObj['eventName'].split('_')[1]
        self.uncommonPrintRun.printUncommonPrintRunInfo(uncommons, setCode)
        uncommonPack = self.uncommonPrintRun.getUncommonPrintRun(uncommons, setCode)
        self.draftPackUpdate.emit(draftPack, uncommonPack)
        print("=======================================================================")
        

if __name__ == '__main__':
    parser = MtgaDraftParser()
    parser.run()
