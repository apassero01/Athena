from .VectorEngine import VectorEngine
from .KBitem import KBItem, TextKBItem, ImageKBItem

class Query: 
    def __init__(self, queryString,userID): 
        self.vectorEngine = VectorEngine()
        self.queryString = queryString 
        self.userID = userID

    
    def getMatchedDocs(self): 
        kbItemIDs = self.vectorEngine.getMatchedDocs(queryString=self.queryString,userID=self.userID)

        kbItemsScore = [] 
        for ID in kbItemIDs: 
            item = KBItem.objects.get(pk=ID)
            kbItemsScore.append((item,kbItemIDs[ID]))
        
        sortedMatchedKbItems = sorted(kbItemsScore, key = lambda x: x[1])
        
        return sortedMatchedKbItems

    
