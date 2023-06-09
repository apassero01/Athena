from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Screenshot import Screenshot
import requests
from selenium.webdriver.common.by import By
from time import sleep

class InputProcessor: 
    def __init__(self, url, userTags = ""): 
        self.url = url 
        self.userTags = userTags
        self.allContent = ""
    
    def parseURL(self):
        driver = webdriver.Chrome()
        driver.get(url)
        sleep(3)

        if "twitter" in url: 
            elements = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")
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

        filename = "textData.txt" 
        textFile = open(filename, 'w')
        textFile.write(allText)
        textFile.close()
        return filename, self.url

    



url = "https://www.allrecipes.com/article/how-to-cook-steak/"
# url = "https://twitter.com/greg_price11/status/1665792769472823299"
processor = InputProcessor(url)
processor.parseURL()
processor.generateTextFile()


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
    
    

