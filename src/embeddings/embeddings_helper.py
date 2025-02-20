from config import openai_client

def get_embedding(text, model="text-embedding-ada-002"):
    response = openai_client.embeddings.create(input=text, model=model)
    return response.data[0].embedding