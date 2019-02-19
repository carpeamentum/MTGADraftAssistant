from PyQt5.QtWidgets import QApplication
import DraftParser
from MtgaDraftAssistantUI import MtgaDraftAssistantUI

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mtgaDraftAssistantUI = MtgaDraftAssistantUI()
    mtgaDraftAssistantUI.displayCards()
    draftParser = DraftParser.MtgaDraftParser()
    draftParser.draftPackUpdate.connect(mtgaDraftAssistantUI.displayPack)
    draftParser.draftCompletion.connect(mtgaDraftAssistantUI.displayCompletionScreen)
    
    draftParser.finished.connect(app.exit)
    draftParser.start()
    sys.exit(app.exec_())
