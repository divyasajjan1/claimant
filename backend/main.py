from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from graph.claim_graph import build_graph
from db.database import init_db
from db.claims_repo import save_claim, get_all_claims
from utils.chunker import chunk_docs
from utils.blob_loader import load_all_docs
from utils.azure_search import create_index, upload_chunks, search_chunks

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"DB init failed: {e} — continuing without DB")
    yield

app = FastAPI(title="Claimant API", lifespan=lifespan)
graph = build_graph()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*",
    #     "http://localhost:3000",
    #     "https://divyasajjan1.github.io"
    # ],
    allow_origins=["https://divyasajjan1.github.io"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

class DisputeRequest(BaseModel):
    raw_input: str


@app.get("/")
def health_check():
    return {"status": "Claimant API is running"}

@app.get("/debug-chunks")
def debug_chunks():
    docs = load_all_docs()
    return chunk_docs(docs)

@app.get("/setup-index")
def setup_index():
    create_index()
    return {"status": "index created"}

@app.get("/upload-chunks")
def upload():
    docs = load_all_docs()
    chunks = chunk_docs(docs)

    upload_chunks(chunks)

    return {"uploaded": len(chunks)}

@app.get("/debug-retrieval")
def debug_retrieval(query: str):
    return search_chunks(query)

@app.post("/dispute")
def submit_dispute(request: DisputeRequest):
    result = graph.invoke({
        "raw_input": request.raw_input,
        "claim": {},
        "verified": False,
        "fraud_score": 0.0,
        "fraud_recommendation": "",
        "decision": "",
        "refund_amount": 0.0,
        "decision_reason": "",
        "customer_message": "",
        "escalation_summary": ""
    })

    try:
        save_claim(result)
        print("Claim saved successfully")
    except Exception as e:
        print(f"DB Error: {e}")

    return {
        "claim": result["claim"],
        "verified": result["verified"],
        "fraud_score": result["fraud_score"],
        "decision": result["decision"],
        "refund_amount": result["refund_amount"],
        "reason": result["decision_reason"],
        "customer_message": result["customer_message"],
        "escalation_summary": result["escalation_summary"]
    }

@app.get("/claims")
def get_claims():
    rows = get_all_claims()
    return {"total": len(rows), "claims": rows}