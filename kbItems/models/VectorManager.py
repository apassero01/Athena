import os 
import dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
import openai 
import pinecone
from langchain.vectorstores import Pinecone

class VectorManager(): 
    def __init__(self): 
        dotenv.load_dotenv()
        pinecone.init(
            api_key = os.getenv("PINECONE_API_KEY"),
            environment = os.getenv("PINECONE_ENV")
        )
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    def textToDocs(self, filePath,uri):
        loader = TextLoader(file_path=filePath)
        documents = loader.load() 
        documents[0].metadata["uri"] = uri
        return documents

    def splitText(self, documents): 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0 ) 
        docuements = text_splitter.split_documents(documents=documents)
        return docuements
    

    def addDocsToIndex(self,index, documents): 
        curURI = documents[0].metadata['uri']

        
        pineconeIndex = pinecone.Index(index_name=index)
        
        db = Pinecone.from_existing_index(index_name=index,embedding=self.embeddings)

        db.add_documents(documents=documents)


        #TODO add try and catch 
        return True  

    
    def removeDocsFromIndex(self,index, docSource): 
        index = pinecone.Index(index_name=index)
        index.delete(filter={"source": docSource})

    def queryDocs(self,index, query):
        
        db = Pinecone.from_existing_index(index_name=index,embedding=self.embeddings)
        results = db.similarity_search(query)
        return results
    
    def emptyIndex(self,index): 
        index = pinecone.Index(index_name=index)
        index.delete(filter = {
        })


    def createEmbeddings(documents):
        dotenv.load_dotenv()
        model_name = 'text-embedding-ada-002'


        docText = [d.page_content for d in documents]
        embed = OpenAIEmbeddings(
            model=model_name,
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )  

        res = embed.embed_documents(docText)

        return res
    
# index = "example1"
# vm = VectorMangager() 
# # vm.emptyIndex(index)
# # vm.removeDocsFromIndex(index = "example1",docSource ="textData.txt")
# documents = vm.textToDocs("textData.txt","www.jumpoffabirdge")
# documents = vm.splitText(documents)
# # # VectorMangager.createEmbeddings(documents=documents)
# vm.addDocsToIndex(index = "example1",documents=documents)
# vm.queryDocs(index = "example1",query="steak")



