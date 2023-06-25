import model.InputProcessor as InputProcessor
import model.QueryProcessor as QueryProcessor 
import model.VectorManager as VectorManager
import os 
import pickle 

class Client: 
    def __init__(self,index): 
        self.inputProcessor = None
        self.vectorManager = VectorManager.VectorMangager() 
        self.queryProcessor = QueryProcessor.QuertyProcessor() 
        self.AllURIs = []

        self.index = index 
    
    def addURI(self,URI, userContent = ""):
        if URI in self.AllURIs:
            return False
        self.inputProcessor = InputProcessor.InputProcessor(URI, userContent)

        #TODO add try catch 
        sucess = self.inputProcessor.parseURL()
        txtFilePath = self.inputProcessor.generateTextFile()

        documents = self.vectorManager.textToDocs(txtFilePath,URI)
        documents = self.vectorManager.splitText(documents)
        success = self.vectorManager.addDocsToIndex(self.index, documents)

        self.AllURIs.append(URI)


    def queryDocuments(self,query): 
        matchedDocs = self.queryProcessor.findResources(query,self.index)
        # for doc in matchedDocs: 
        #     print(doc.page_content)
        return matchedDocs


def main(): 
    index = "example1"  
    if os.path.exists("testUserData.pkl"):
        client = loadClient()
        client.vectorManager = VectorManager.VectorMangager()
    else: 
        client = Client(index)

    # url = "https://www.allrecipes.com/article/how-to-cook-steak/"
    urls = ["https://twitter.com/greg_price11/status/1665792769472823299","https://twitter.com/taxcredithunter/status/1667955089829445632?s=20",
            "https://twitter.com/historyinmemes/status/1667972857626865668?s=20","https://twitter.com/BleacherReport/status/1668047841997230080?s=20",
            "https://www.instagram.com/reel/CrXgAazgKJ0/","https://www.instagram.com/reel/CtPit6CsH6F/?igshid=ZjUwM2YwMzA3MA%3D%3D",
            "https://www.instagram.com/reel/Cq_396XM1tv/?igshid=ZjUwM2YwMzA3MA%3D%3D","https://www.instagram.com/reel/Cq3ZENVugK9/?igshid=ZjUwM2YwMzA3MA%3D%3D",
            "https://www.active.com/fitness/articles/10-weightlifting-exercises-for-beginners"]
    for url in urls:
        client.addURI(url)
    client.queryDocuments("how to lift ")
    saveClient(client=client)


def loadClient():
    return pickle.load(open("testUserData.pkl","rb"))

def saveClient(client):
    pickle.dump(client,open("testUserData.pkl","wb"))

# main()