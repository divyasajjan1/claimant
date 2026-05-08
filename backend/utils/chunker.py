from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = []

    for doc in docs:
        split_texts = splitter.split_text(doc["text"])

        for i, chunk in enumerate(split_texts):
            chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })

    return chunks