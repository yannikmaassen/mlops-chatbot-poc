import nltk
from nltk.tokenize import sent_tokenize
nltk.download("punkt")

def chunk_text(text, max_words=300):
    sentences = sent_tokenize(text)
    chunks, current_chunk = [], []
    word_count = 0
    
    for sentence in sentences:
        words = sentence.split()
        word_count += len(words)
        
        if word_count > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            word_count = len(words)
        
        current_chunk.append(sentence)
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def search_docs(collection, query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    if not results["documents"] or len(results["documents"][0]) == 0:
        return ["No relevant documents found."]
    
    return results["documents"][0]