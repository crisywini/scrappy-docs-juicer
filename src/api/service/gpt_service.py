from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.chat_models import ChatOpenAI
import os

#with open('../data/external/gpt-credentials.txt') as f:
#    key = f.read()



class GPTAdapter:

    def __init__(self, open_ai_key:str):
        self.open_ai_key = open_ai_key
        os.environ['OPENAI_API_KEY'] = self.open_ai_key

    def query(self, context_path: str,  query:str):
        prompt = "Hello! please answer this question following the next documentation, please generate the answer in semantic html. " + query
        loader = TextLoader(context_path, encoding='utf8')
        index = VectorstoreIndexCreator().from_loaders([loader])
        return index.query(prompt, llm=ChatOpenAI())
