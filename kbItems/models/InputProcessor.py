from bs4 import BeautifulSoup
from selenium import webdriver
import re
# from selenium.webdriver.chrome.options import Options
# from Screenshot import Screenshot
# import requests
from selenium.webdriver.common.by import By
from time import sleep

class InputProcessor: 
    def __init__(self, url, userTags = ""): 
        self.url = url 
        self.userTags = userTags
        self.allContent = ""
    
    def parseURL(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        sleep(3)

        if "twitter" in self.url: 
            elements = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")
            for e in elements:
                    self.allContent = self.allContent + e.text + "\n"
        if "instagram" in self.url: 
            elements = driver.find_elements(By.XPATH,"//meta[@property='og:title']")
            for e in elements:
                pattern = re.compile(r'[^A-Za-z0-9\s\n]+')
                content = pattern.sub("",e.get_attribute("content"))
                self.allContent = self.allContent + content + "\n"
        else:
            allTags = ["p", "h", "title"]
            elements = [] 
            for tag in allTags: 
                elements += driver.find_elements(By.TAG_NAME,tag)
                for e in elements:
                    self.allContent = self.allContent + e.text + "\n"
    
    
        

        driver.close()
        driver.quit()


        #Add try and catch statements to determine if webscrape was successful    
        isSuccess = len(self.allContent) > 0
        return isSuccess ,self.allContent 

    def generateTextFile(self): 
        allText = self.userTags + "\n" + self.allContent

        filePath = "textData.txt" 
        textFile = open(filePath, 'w')
        textFile.write(allText)
        textFile.close()
        return filePath
    

    



# url = "https://www.allrecipes.com/article/how-to-cook-steak/"
# # url = "https://twitter.com/greg_price11/status/1665792769472823299"
# url = "https://www.instagram.com/reel/CrXgAazgKJ0/"
# processor = InputProcessor(url)
# processor.parseURL()
# processor.generateTextFile()


#Regular website idea
# def parseURL(self):
    #     response = requests.get(self.url) 
    #     html_content = response.content 
    #     soup = BeautifulSoup(html_content, 'html.parser')


    #     allContent = "" 
    #     allTags = ["p", "h", "title"]
    #     for tag in allTags: 
    #         curText = soup.get_text(tag)
    #         curText = curText.replace(tag, "").replace("\n", "")
            
    #         allContent += "\n"
    #         allContent += curText
        
    #     print(allContent)
    
    

