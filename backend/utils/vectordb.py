import chromadb
from backend.utils.embeddings import embedding_model

client = chromadb.Client()

collection = client.get_or_create_collection("claim_policies")

def store_chunks(chunks):
    texts = [c["text"] for c in chunks]

    embeddings = embedding_model.embed_documents(texts)

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=[f"chunk-{i}" for i in range(len(chunks))]
    )

def search_chunks(query, k=3):
    query_embedding = embedding_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results