import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

escalation_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a banking escalation specialist.
    Prepare a complete summary for the human adjuster.
    
    Respond ONLY with valid JSON:
    {{
        "priority": "low / medium / high",
        "summary": "full case summary for adjuster",
        "recommended_action": "what the adjuster should do",
        "estimated_resolution_days": 1-30
    }}
    """),
    ("human", """
    Claim: {claim}
    Verified: {verified}
    Fraud score: {fraud_score}
    Decision reason: {reason}
    """)
])

escalation_chain = escalation_prompt | llm | JsonOutputParser()

def run_escalation(claim: dict, verified: bool, fraud_score: float, reason: str) -> dict:
    return escalation_chain.invoke({
        "claim": str(claim),
        "verified": verified,
        "fraud_score": fraud_score,
        "reason": reason
    })