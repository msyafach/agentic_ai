import getpass 
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.retrievers import BM25Retriever
from dotenv import load_dotenv

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")


class llm:

    def __init__(self, llm_model:str ):
        self.llm_model = ChatGoogleGenerativeAI(model=llm_model,
                                                api_key=os.getenv("GOOGLE_API_KEY"),
                                                temperature=0.0,
                                                max_tokens=None,
                                                timeout=None,
                                                max_retries=2)
        
    
    

