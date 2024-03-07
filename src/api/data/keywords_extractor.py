
from transformers import pipeline
from rake_nltk import Rake


class PiKeyWordsGenerator:

    def __init__(self, context: str):
        self.context = context
        
    
    def get_keywords(self) -> list:
        # Initialize the text summarization pipeline
        #summarization_pipeline = pipeline("summarization")

        # Sample input text
        #summary = summarization_pipeline(self.context,
        #                                  max_length=100, min_length=30, do_sample=False)
        r = Rake()
        #r.extract_keywords_from_text(summary[0]["summary_text"])
        r.extract_keywords_from_text(self.context)
        return r.get_ranked_phrases()