from config import openai_client
from embeddings import get_embedding
from retriever import search_docs
from database import initialize_chromadb

def generate_response(query):
    collection = initialize_chromadb()
    query_embedding = get_embedding(query)
    relevant_docs = search_docs(collection, query_embedding)

    if relevant_docs == ["No relevant documents found."]:
        return "I couldn't find relevant documentation. Try rephrasing your question."

    context = "\n\n".join(relevant_docs)
    prompt = f"""You are an expert in MLOps. Use the following documentation to answer the question.

    Context:
    {context}

    Question: {query}
    """

    try:
        response = openai_client.chat.completions.create(model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI assistant specialized in MLOps."},
                  {"role": "user", "content": prompt}])
        return response.choices[0].message.content

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "An error occurred while generating the response."