from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os
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
        # self.llm = ChatOpenAI(model_name = 'text-davinci-003')
        self.llm = OpenAI()
    
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
        
    


    

        
    
