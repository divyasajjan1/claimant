from utils.azure_search import search_chunks

def run_rules_lookup(raw_input: str) -> str:
    retrieved_chunks = search_chunks(raw_input)
    print("RULES AGENT ACTIVE")
    context = "\n\n".join([
        f"[Source: {c['source']}]\n{c['content']}"
        for c in retrieved_chunks
    ])

    print("RULES CONTEXT:", context[:300])
    return context