from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os
import re
from dotenv import load_dotenv


class Agent: 
    '''
    Agent class allowing for user to interact with LLM via prompt templates and text input 
    '''
    def __init__(self): 
        '''
        Load environment varaibles including API key for LLM. Currently using ChatGPT but can change
        '''
        load_dotenv() 
        self.llm = ChatOpenAI(model_name = 'gpt-4')
        # self.llm = OpenAI(model_name='gpt-4')
    
    def trimItemContent(self,itemContent): 
        '''
        Prompt template taking text user input and trimming all irrelivent text from web scraping
        '''
        trimContentPromt = PromptTemplate(
        input_variables = ["text_input"],
        template = "take this string of content scraped from a screenshot and return update it to a string" 
        "that only has information relevent to the post:  \n {text_input}" 
        )

        trimpContentChain = LLMChain(llm=self.llm, prompt = trimContentPromt)
        return trimpContentChain.run(itemContent) 
    
    def createItemTags(self,itemContent):
        '''
        Promt template taking text input and creating additional context from text input
        '''
        if len(itemContent) > 1250: 
            itemContent = itemContent[250:1250] 
        CreateItemTagPrompt = PromptTemplate(
        input_variables = ["text_input"],
        template = "Return NO MORE THAN 200 CHARACTERS containing the most relevant tags to the following information: {text_input} " 
        )
        CreateTagChain = LLMChain(llm=self.llm, prompt = CreateItemTagPrompt)
        tags = CreateTagChain.run(itemContent)
        return tags 
    
    def generateTitleAndSource(self,itemContent,URI): 
        '''
        Prompt template taking text input and generating a title for the document
        '''
        if len(itemContent) > 1250: 
            itemContent = itemContent[0:1250] 
        GenerateTitlePrompt = PromptTemplate(
        input_variables = ["text_input"],
        template = "Generate a title relevant to the item content only and give the source of this item such as the platform or website: ie Instangram. Put the response and platform together inside [] and separate the two by '::' Input: {text_input} " 
        )

        prompt = "URL: " + URI + "\n" + "Content: " + itemContent
        GenerateTitleChain = LLMChain(llm=self.llm, prompt = GenerateTitlePrompt)
        response = GenerateTitleChain.run(prompt)

        match = re.search(r'\[(.*?)\]', response)

        if match:
            response = match.group(1)
        else:
            response = response

        response = response.replace('"','')
        title = response.split("::")[0]
        source = response.split("::")[1]
        print("title: " +  title + " source: " + source)
        return title,source

        
    


    

        
    
