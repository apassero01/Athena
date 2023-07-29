import threading
from .models.KBitem import KBItem, TextKBItem, ImageKBItem

class KBItemBackground(threading.Thread): 
    def __init__(self, kbItem): 
        self.kbItem = kbItem
        threading.Thread.__init__(self)
    
    def run(self): 
        try: 
            print('Background thread started') 
            self.createItem()
            print('Thread complete')
        except Exception as e: 
            print(e)

    def createItem(self): 
        self.kbItem.userID = 1
        self.kbItem.save() 
        self.kbItem.parseURI()
        self.kbItem.save() 
        self.kbItem.createVector()
