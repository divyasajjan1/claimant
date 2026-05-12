import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


approval_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a senior banking dispute resolution specialist.
    Make a final decision on the claim based on all evidence.
    
    Rules:
    - If verified=false → reject
    - If fraud_score >= 0.8 and recommendation=investigate → escalate
    - If fraud_score >= 0.9 → reject
    - If fraud_score < 0.4 and verified=true → approve
    - Otherwise → escalate
    
    Respond ONLY with valid JSON. 
    You MUST cite policy sources using [Source: ...] format from provided context.:
    {{
        "decision": "approve / reject / escalate",
        "refund_amount": 0.0,
        "reason": "brief explanation",
        "next_step": "what happens next",
        "citations": ["policy1.pdf", "policy2.pdf"]
    }}
    """),
    ("human", """
    Relevant banking policies: {policy_context}
    Claim: {claim}
    Verified: {verified}
    Fraud score: {fraud_score}
    Fraud recommendation: {fraud_recommendation}
    """)
])

approval_chain = approval_prompt | llm | JsonOutputParser()


def run_approval(claim: dict, verified: bool, fraud_score: float, fraud_recommendation: str, policy_context: str) -> dict:
    return approval_chain.invoke({
        "policy_context": policy_context,
        "claim": str(claim),
        "verified": verified,
        "fraud_score": fraud_score,
        "fraud_recommendation": fraud_recommendation
    })