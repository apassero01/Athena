from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from langchain.document_loaders.image import UnstructuredImageLoader
from django.db import models
from .VectorEngine import VectorEngine
import os



class KBItem(models.Model):
    URI = models.CharField(max_length = 500) 
    userTags = models.CharField()
    itemContent = models.TextField(default="")
    vectorEngine = VectorEngine()

        
    def parseURI(self): 
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options = chrome_options)
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})

    
    def addURI(self,URI, userTags = ""): 
        self.URI = URI; 
        self.userTags = userTags
        self.itemContent = ""

    
    def addUserTags(self,userTags): 
        self.userTags = userTags
    
    def createVector(self): 
        self.vectorEngine = VectorEngine() 

        documents = self.vectorEngine.TextToDocs(self.itemContent,self.id)
        
        self.vectorEngine.storeVector(documents)



class ImageKBItem(KBItem): 
    
    def parseURI(self):
        super().parseURI()
        self.driver.set_window_size(1920, 1080)
        self.driver.get(self.URI)
        
        time.sleep(3)
        self.driver.save_screenshot('screen_shot.png')

        self.driver.close()
        self.driver.quit()

        loader = UnstructuredImageLoader("screen_shot.png")
        data = loader.load() 
        os.remove("screen_shot.png")

        for ele in data: 
            self.itemContent = self.itemContent + " " + ele.page_content   

        
class TextKBItem(KBItem): 
    
    def parseURI(self): 
        super().parseURI()
        self.driver.get(self.URI)
        elements = [] 
        allTags = ["p", "h", "title"]
        for tag in allTags: 
            elements += self.driver.find_elements(By.TAG_NAME,tag)
            for e in elements:
                self.itemContent = self.itemContent + e.text + "\n"

        self.driver.close()
        self.driver.quit()

# url = "https://twitter.com/Travis_in_Flint/status/1674890906372132864?s=20"
# textTest = ImageKBItem()
# textTest.addURI(url)
# textTest.parseURI()
