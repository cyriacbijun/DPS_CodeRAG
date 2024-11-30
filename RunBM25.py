# BM25 implementation
import json
from rocksdbpy import rocksdbpy
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize

def preprocess_text(text):
    """Preprocess text by tokenizing and stripping whitespace."""
    text = text.strip()
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return word_tokenize(text.lower())  # Tokenize and lowercase for BM25

def rank_bm25_search(db_path, query_code, top_k=1):
    """Perform a BM25 search on stored code snippets and return the top k most similar."""
    # Open the RocksDB database
    db = rocksdbpy.open_default(db_path)

    # Retrieve all code snippets from RocksDB
    all_code_snippets = []
    i = 0
    while True:  # Iterate until we reach a key that doesn't exist
        key = i.to_bytes(2, 'big')  # Assuming keys are 2-byte integers
        value = db.get(key)
        if value is None:
            break  # Stop if key doesn't exist
        data_dict = json.loads(value.decode('utf-8'))
        code_snippet = data_dict.get("code", "")
        all_code_snippets.append(code_snippet)
        i += 1

    # Preprocess the query and the stored code snippets
    all_tokens = [preprocess_text(snippet) for snippet in all_code_snippets]
    query_tokens = preprocess_text(query_code)

    # Create BM25 model using the code snippets
    bm25 = BM25Okapi(all_tokens)

    # Get BM25 scores for the query
    scores = bm25.get_scores(query_tokens)

    # Get top k most similar code snippets based on BM25 scores
    top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    # Fetch the top k results from RocksDB
    top_k_results = []
    for idx in top_k_indices:
        print("SCORE : ", scores[idx])
        key = idx.to_bytes(2, 'big')
        value = db.get(key)
        if value:
            data_dict = json.loads(value.decode('utf-8'))
            top_k_results.append(data_dict)

    return top_k_results

#query_code = "def sum(a, b): return a + b"  # Replace with user query
def query_bm25(query):
    top_k_results = rank_bm25_search("test_db", query, top_k=1)
    return top_k_results

