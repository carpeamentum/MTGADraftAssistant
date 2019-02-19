from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QMainWindow, QAction
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

from CardMap import CardMap
from DraftPublisher import DraftPublisher

class MtgaDraftAssistantUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.updateCards)
        self.draftPublisher = DraftPublisher()

        self.fileMenu = self.menuBar().addMenu('File')
        self.exportDraftAction = QAction('Export Draft')
        self.fileMenu.addAction( self.exportDraftAction )
        self.exportDraftAction.triggered.connect(self.draftPublisher.exportFile)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.grid = QGridLayout(self.mainWidget)
        self.packLabel = QLabel("Draft Pack:")
        font = self.packLabel.font()
        font.setPointSize(32)
        font.setBold(True)
        self.packLabel.setFont(font)
        
        self.uncommonsLabel = QLabel("Possible Missing Uncommons:")
        font = self.uncommonsLabel.font()
        font.setPointSize(24)
        font.setBold(True)
        self.uncommonsLabel.setFont(font)
        self.packCards = []
        self.uncommonCards = []
        self.loadNumberPixmaps()
        
        self.completedLabel = QLabel("Draft Complete.  Draft log located at:")
        font = self.packLabel.font()
        font.setPointSize(20)
        font.setBold(True)
        self.completedLabel.setFont(font)

        self.completedDraftlogFilenameLabel = QLabel("Filename Not Set")
        font = self.packLabel.font()
        font.setPointSize(20)
        font.setBold(True)
        self.completedDraftlogFilenameLabel.setFont(font)

        self.exportDraftButton = QPushButton('Export Draft File')
        self.exportDraftButton.clicked.connect(self.exportButtonClicked)
        self.exportDraftButton.hide()
        

        self.setWindowTitle("MTGA Draft Assistant")
        self.show()

    def displayCards(self):
        self.grid.addWidget(self.packLabel,0,0,1,3)
        self.packLabel.show()
        self.clearCompletionScreen()
        for i, card in enumerate(self.packCards):
            if i<8:
                self.grid.addWidget(card['ownedLabel'], 1, i)
                self.grid.addWidget(card['label'], 2, i)
            else:
                self.grid.addWidget(card['ownedLabel'], 3, i-8)
                self.grid.addWidget(card['label'], 4, i-8)
        if self.uncommonCards:
            self.grid.addWidget(self.uncommonsLabel,5,0,1,3)
            self.uncommonsLabel.show()
            for i, card in enumerate(self.uncommonCards):
                self.grid.addWidget(card['label'], 6, i)
        else:
            self.grid.removeWidget(self.uncommonsLabel)
            self.uncommonsLabel.hide()


    def updateCards(self, replyObject):
        data = replyObject.readAll()
        iPixmap = QPixmap()
        iPixmap.loadFromData(data, 'jpg')
        
        cardImageLabel= QLabel()
        cardImageLabel.setPixmap(iPixmap)
        replyUrlString = replyObject.url().toString()

        for cardLabelPair in self.packCards:
            if replyUrlString == self.getCardImageUrl(cardLabelPair['card']):
                cardLabelPair['label'] = cardImageLabel
        for cardLabelPair in self.uncommonCards:
            if replyUrlString == self.getCardImageUrl(cardLabelPair['card']):
                cardLabelPair['label'] = cardImageLabel

        self.sortPack()
        self.displayCards()
        self.show()

    def downloadImage(self, url, processImage):
        if url is str:
            imageUrl = QUrl(url)
        else:
            imageUrl = url
        self.request = QNetworkRequest()
        self.request.setUrl(QUrl(imageUrl))
        self.replyObject = self.manager.get(self.request)

    @pyqtSlot(str)
    def displayCompletionScreen(self, completedDraftFilename):
        self.completedDraftFilename = completedDraftFilename
        
        self.clearPack()
        self.grid.removeWidget(self.uncommonsLabel)
        self.uncommonsLabel.hide()
        self.uncommonsLabel.setParent(None)
        self.grid.removeWidget(self.packLabel)
        self.packLabel.hide()
        self.packLabel.setParent(None)

        self.grid.addWidget(self.completedLabel,0,0,1,3)
        self.completedLabel.show()

        self.completedDraftlogFilenameLabel.setText(completedDraftFilename)
        self.grid.addWidget(self.completedDraftlogFilenameLabel,1,0,1,3)
        self.completedDraftlogFilenameLabel.show()

        self.grid.addWidget(self.exportDraftButton,2,0,1,2)
        self.exportDraftButton.show()
        

    @pyqtSlot(list, list)
    def displayPack(self, draftPack, uncommons):
##        print('displayPack')
        self.clearPack()
        for card in draftPack:
            c=dict(card)
            ownedLabel = QLabel()
            ownedLabel.setPixmap(self.numberPixmaps[int(c['owned'])])
            self.packCards.append({'card':c, 'label':QLabel(), 'ownedLabel':ownedLabel})
            self.downloadImage(self.getCardImageUrl(c), self.updateCards)
        for card in uncommons:
            c=dict(card)
            self.uncommonCards.append({'card':c, 'label':QLabel()})
            self.downloadImage(self.getCardImageUrl(c), self.updateCards)

    def clearCompletionScreen(self):
        self.grid.removeWidget(self.completedLabel)
        self.completedLabel.hide()
        self.completedLabel.setParent(None)
        
        self.grid.removeWidget(self.completedDraftlogFilenameLabel)
        self.completedDraftlogFilenameLabel.hide()
        self.completedDraftlogFilenameLabel.setParent(None)
        
        self.grid.removeWidget(self.exportDraftButton)
        self.exportDraftButton.hide()
        self.exportDraftButton.setParent(None)

    def exportButtonClicked(self):
        print('clicked')
        print(self.completedDraftFilename)
        self.draftPublisher.exportFile(draftLogFile = self.completedDraftFilename)
        

    def clearPack(self):
        for card in self.packCards:
            self.grid.removeWidget(card['label'])
            card['label'].hide()
            card['label'].setParent(None)
            self.grid.removeWidget(card['ownedLabel'])
            card['ownedLabel'].hide()
            card['ownedLabel'].setParent(None)
        for card in self.uncommonCards:
            self.grid.removeWidget(card['label'])
            card['label'].hide()
            card['label'].setParent(None)

        self.uncommonCards = []
        self.packCards = []

    def cardLabelPairSortKey(cardLabelPair):
        return CardMap.cardSortKey(cardLabelPair['card'])

    def sortPack(self):
        self.packCards.sort(key=MtgaDraftAssistantUI.cardLabelPairSortKey)
        
    def getCardImageUrl(self, card):
        return card['images'][0]['small']

    def loadNumberPixmaps(self):
        self.numberPixmaps = []
        for i in range(5):
            nPixmap = QPixmap()
            nPixmap.load('numbers/'+str(i)+'.jpg')
            self.numberPixmaps.append(nPixmap)
            
        
