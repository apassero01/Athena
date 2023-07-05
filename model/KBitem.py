from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from langchain.document_loaders.image import UnstructuredImageLoader
from django.db import models


class KBItem(models.Model):
    URI = models.CharField(max_length = 500) 
    userTags = models.CharField()
    def __init__(self,URI, userTags = ""): 
        self.URI = URI; 
        self.userTags = userTags
        self.itemContent = ""
        

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options = chrome_options)
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})

        
    
    def parseURI(): 
        pass
    



class ImageKBItem(KBItem): 
    def __init__(self,URI, userTags = ""):
        super().__init__(URI, userTags = "")
    
    def parseURI(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get(self.URI)
        
        time.sleep(3)
        self.driver.save_screenshot('screen_shot.png')

        self.driver.close()
        self.driver.quit()

        loader = UnstructuredImageLoader("screen_shot.png")
        data = loader.load() 

        for ele in data: 
            self.itemContent = self.itemContent + " " + ele.page_content   

        
class TextKBItem(KBItem): 
    def __init__(self,URI, userTags = ""):
        super().__init__(URI, userTags = "") 
    
    def parseURI(self): 
        self.driver.get(self.URI)
        elements = [] 
        allTags = ["p", "h", "title"]
        for tag in allTags: 
            elements += self.driver.find_elements(By.TAG_NAME,tag)
            for e in elements:
                self.itemContent = self.itemContent + e.text + "\n"

        self.driver.close()
        self.driver.quit()

url = "https://twitter.com/Travis_in_Flint/status/1674890906372132864?s=20"
textTest = ImageKBItem(url)
textTest.parseURI()
print(textTest.itemContent)