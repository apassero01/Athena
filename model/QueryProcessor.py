import VectorManager as vm

class QuertyProcessor: 
    def __init__(self): 
        self.vectorManager = vm.VectorMangager()

    def findResources(self,query,index): 
        matchedDocs = self.vectorManager.queryDocs(index,query)
        return matchedDocs 
    

    
