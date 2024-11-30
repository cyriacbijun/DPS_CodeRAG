import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def preprocess_text(text):
    """Preprocess text by stripping whitespace and normalizing line endings."""
    text = text.strip()
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text

# Querying the FAISS index for the most similar functions
def search_similar_function(query, k=3):
    # Convert query to vector embedding
    query_embedding = model.encode([query]).astype('float32')
    
    # Perform the search in the FAISS index
    distances, indices = index.search(query_embedding, k)
    
    # Return the top k most similar functions along with their indices
    return indices[0], distances[0]


# Loading the FAISS index 
index = faiss.read_index("./python_functions_index.faiss")   # FIX THE PATH
model = SentenceTransformer('all-MiniLM-L6-v2')

#query = "def sum(a, b): return a + b" # FIX THIS. Get a query from the interface we are developing down the line
def query_faiss(query):
    # Use the indices returned below to get the data from RockDB
    indices, distances = search_similar_function(preprocess_text(query), k=3)
    
    return indices, distances
