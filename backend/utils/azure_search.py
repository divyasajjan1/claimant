# azure_search.py

import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)

from azure.search.documents.models import VectorizedQuery

from langchain_huggingface import HuggingFaceEmbeddings


# -------------------
# config
# -------------------
endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = "claim-policies"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -------------------
# index creation
# -------------------
def create_index():
    client = SearchIndexClient(endpoint, AzureKeyCredential(key))

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),

        SearchField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True
        ),

        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=384,
            vector_search_profile_name="default"
        )
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="default")],
        profiles=[VectorSearchProfile(name="default", algorithm_configuration_name="default")]
    )

    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search
    )

    client.create_or_update_index(index)


# -------------------
# upload chunks
# -------------------
def upload_chunks(chunks):
    client = SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(key)
    )

    docs = []

    for i, c in enumerate(chunks):
        vec = embedding_model.embed_query(c["text"])

        docs.append({
            "id": str(i),
            "content": c["text"],
            "contentVector": vec
        })

    client.upload_documents(docs)

def search_chunks(query, k=3):
    client = SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(key)
    )

    query_vector = embedding_model.embed_query(query)

    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=k,
        fields="contentVector"
    )

    results = client.search(
        search_text="",
        vector_queries=[vector_query]
    )

    return [
        {
            "content": r["content"],
            "score": r["@search.score"]
        }
        for r in results
    ]