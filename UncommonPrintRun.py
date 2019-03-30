from CardMap import CardMap

printRunFilenames = {'RNA': "uncommonData/mtg_arena_rna_uncommon_print_run.txt",
                     'GRN': "uncommonData/mtg_arena_grn_uncommon_print_run.txt",
                     'M19': "uncommonData/mtg_arena_m19_uncommon_print_run.txt",
                     'DOM': "uncommonData/mtg_arena_dom_uncommon_print_run.txt",
                     'RIX': "uncommonData/mtg_arena_rix_uncommon_print_run.txt",
                     'XLN': "uncommonData/mtg_arena_xln_uncommon_print_run.txt"}


class UncommonPrintRun():
    def __init__(self, cardMap):
        self.printRunData = {}
        self.cardMap = cardMap
    
    def loadPrintRunData(self, setCode):
        setCode = setCode.upper()
        self.printRunData[setCode] = []
        with open(printRunFilenames[setCode]) as f:
            line = f.readline()
            while not "" == line:
                self.printRunData[setCode].append(line.strip())
                line = f.readline()

    def printRunIndexer(self, setCode, index):
        setCode = setCode.upper()
        if index <0:
            return len(self.printRunData[setCode])+index-1
        elif index >= len(self.printRunData[setCode]):
            return index - len(self.printRunData[setCode])
        else:
            return index

    def printUncommonPrintRunInfo(self, uncommons, setCode):
        setCode = setCode.upper()
        printruninfo = self.getUncommonPrintRun(uncommons, setCode)
        if printruninfo:
            if len(printruninfo) == 1:
                print("The Missing uncommon is:  " + printruninfo[0]['name'])
            else:
                print("Possible missing uncommons: ")
                for card in printruninfo:
                    print(card['name'])

    def getUncommonPrintRun(self, uncommons, setCode):
        setCode = setCode.upper()
        if setCode not in self.printRunData:
            if setCode in  printRunFilenames:
                self.loadPrintRunData(setCode)
            else:
                return([])
        printRunInfo = []
        if len(uncommons) == 2:
            index1 = self.printRunData[setCode].index(uncommons[0]['name'])
            index2 = self.printRunData[setCode].index(uncommons[1]['name'])
            if index1 > index2:
                x = index1
                index1 = index2
                index2 = x
            indexDiff = index2-index1
            if index1 <2 and index2 > (len(self.printRunData[setCode])-3):
                indexDiff = (len(self.printRunData[setCode])-index1) - index2
                x = index1
                index1 = index2
                index2 = x        
            if indexDiff == 1:

                printRunInfo.append(self.cardMap.getCardInfoByName(self.printRunData[setCode][self.printRunIndexer(setCode, index1-1)]))
                printRunInfo.append(self.cardMap.getCardInfoByName(self.printRunData[setCode][self.printRunIndexer(setCode, index2+1)]))
            elif indexDiff == 2:
                printRunInfo.append(self.cardMap.getCardInfoByName(self.printRunData[setCode][self.printRunIndexer(setCode, index1+1)]))
            else:
                print("Uncommon Print Run Error Detected, print runs may no longer be valid")
        elif len(uncommons) == 1:
            index = self.printRunData[setCode].index(uncommons[0]['name'])
            printRunInfo.append(self.cardMap.getCardInfoByName(self.printRunData[setCode][self.printRunIndexer(setCode, index-2)]))
            printRunInfo.append(self.cardMap.getCardInfoByName(self.printRunData[setCode][self.printRunIndexer(setCode, index-1)]))
            printRunInfo.append(self.cardMap.getCardInfoByName(self.printRunData[setCode][self.printRunIndexer(setCode, index+1)]))
            printRunInfo.append(self.cardMap.getCardInfoByName(self.printRunData[setCode][self.printRunIndexer(setCode, index+2)]))
            
        return(printRunInfo)

