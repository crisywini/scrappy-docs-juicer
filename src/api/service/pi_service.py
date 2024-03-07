from service.gpt_service import GPTAdapter
from data.semantic_search import PiSemantica
from data.keywords_extractor import PiKeyWordsGenerator
import pandas as pd

class Pi:

    def __init__(self):
        key = 'api-key'
        self.gpt_adapter = GPTAdapter(key)

    def create_context(self, question:str) -> str:
        
        data_path = 'scrappy-docs-juicer/data/raw/idcloud-content-script.csv'
        df = pd.read_csv(data_path)

        pi_semantica_question = PiSemantica(question, df)        
        # Get the most related articles using bert
        most_related_articles_from_question = pi_semantica_question.find_most_related_articles()
        # Generate keywords
        pi_keyword_generator = PiKeyWordsGenerator(question)
        keywords = pi_keyword_generator.get_keywords()
        # Generate the articles based on the keywords
        keyword = " ".join(keywords)
        pi_semantica_keywords = PiSemantica(keyword, df)        
        most_related_articles_from_keywords = pi_semantica_keywords.find_most_related_articles()
        most_related_articles = most_related_articles_from_keywords + most_related_articles_from_question
        return " ".join(most_related_articles)
    
    def answer(self, question:str) -> str:
        #Create the context
        context = self. create_context(question)
        f = open("context.txt", "a")
        f.write(context)
        f.close()
        return self.gpt_adapter.query("context.txt", question)
    
    