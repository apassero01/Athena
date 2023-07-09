from .VectorManager import VectorManager as vm

class QueryProcessor: 
    def __init__(self): 
        self.vectorManager = vm.VectorManager()

    def findResources(self,query,index): 
        matchedDocs = self.vectorManager.queryDocs(index,query)
        return matchedDocs 
    

    
