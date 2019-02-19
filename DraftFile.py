import json
import os

def loadDraftFile(filename):
    draftFileJson = {}
    try:
        if os.path.dirname(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename) as f:
            draftFileJson = json.load(f)
    except IOError:
        None
    return draftFileJson

def writeDraftFile(filename, draftData):
    with open(filename, 'w+') as f:
        json.dump(draftData,f)

def updateDraftFile(draftStatus):
    filename=getIncompleteDraftFilename(draftStatus)
    draftData = loadDraftFile(filename)
    draftData['p'+str(draftStatus['packNumber'])+'p'+str(draftStatus['pickNumber'])] = draftStatus
    writeDraftFile(filename, draftData)

def getIncompleteDraftFilename(draftStatus):
    return ('DraftLogs/'+draftStatus['draftId']+'.json').replace(':','-')

def updateDraftFileDeck(draftDeckUpdate, filename):
    draftData = loadDraftFile(filename)
    draftData['deck'] = draftDeckUpdate['CourseDeck']
    writeDraftFile(filename, draftData)
    

def updateDraftDeck(draftDeckUpdate):
    idFileName = 'DraftLogs/'+draftDeckUpdate['Id']+".json"
    try:
        updateDraftFileDeck(draftDeckUpdate, idFileName)
        return idFileName
    except IOError:
        preFinalDraftFilename = ('DraftLogs/'+draftCompletion['ModuleInstanceData']['DraftInfo']['DraftId']+'.json').replace(':','-')
        updateDraftFileDeck(draftDeckUpdate, preFinalDraftFilename)
        return preFinalDraftFilename

def finalizeDraft(draftCompletion):
    filename=('DraftLogs/'+draftCompletion['ModuleInstanceData']['DraftInfo']['DraftId']+'.json').replace(':','-')
    draftData = loadDraftFile(filename)
    draftData['deck'] = draftCompletion['CourseDeck']
    writeDraftFile(filename, draftData)
    finalDraftFileName= 'DraftLogs/'+draftCompletion['Id']+".json"
    os.replace(filename, finalDraftFileName)
    return finalDraftFileName
    
