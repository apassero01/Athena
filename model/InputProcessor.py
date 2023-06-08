from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Screenshot import Screenshot
import requests

class InputProcessor: 
    def __init__(self, url, userTags = ""): 
        self.url = url 
        self.userTags = userTags
    
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

    def parseURL(self):

        chrome_options = Options() 
        # chrome_options.add_argument("--headless")
        
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        ob = Screenshot.Screenshot()
        img_url = ob.full_screenshot(driver, save_path=r'.', image_name='myimage.png', is_load_at_runtime=True,
                                          load_wait_time=3)
        driver.close()
        driver.quit()


url = "https://www.allrecipes.com/article/how-to-cook-steak/"
# url = "https://twitter.com/greg_price11/status/1665792769472823299"
processor = InputProcessor(url)
processor.parseURL()

    
    

