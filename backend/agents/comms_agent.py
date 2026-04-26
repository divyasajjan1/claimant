import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    #api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

comms_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a banking customer communication specialist.
    Draft a professional, empathetic message to the customer about their dispute status.
    
    Respond ONLY with valid JSON:
    {{
        "subject": "email subject line",
        "message": "full message to customer",
        "action_required": true/false
    }}
    """),
    ("human", """
    Claim: {claim}
    Decision: {decision}
    Reason: {reason}
    """)
])

comms_chain = comms_prompt | llm | JsonOutputParser()

def run_comms(claim: dict, decision: str, reason: str) -> dict:
    return comms_chain.invoke({
        "claim": str(claim),
        "decision": decision,
        "reason": reason
    })