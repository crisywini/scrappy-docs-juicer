from datasets import load_dataset
from sentence_transformers import SentenceTransformer, util
import torch
import os
import pandas as pd


class PiSemantica:

    def __init__(self, context: str, df: pd.DataFrame):
        
        self.context = context
        self.df = df
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.passage_embeddings = list(self.model.encode(self.df['content'].to_list(),
                                                          show_progress_bar=True))


    def find_most_related_articles(self):
        # Encode the query using the sentence transformer model
        query_embedding = self.model.encode(self.context)
        # Print the shape of the query embedding
        # query_embedding.shape

        # Calculate the cosine similarity between the query embedding and the passage embeddings
        similarities = util.cos_sim(query_embedding, self.passage_embeddings)

        # Find the indices of the top 3 most similar passages
        top_indicies = torch.topk(similarities.flatten(), 3).indices

        # Get the top 3 relevant passages by slicing the summaries at 200 characters and adding an ellipsis
        top_relevant_passages = [self.df.iloc[x.item()]['content'][:200] + "..." for x in top_indicies]

        # Return the top 3 relevant passages
        return top_relevant_passages