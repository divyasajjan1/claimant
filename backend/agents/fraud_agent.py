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

fraud_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a banking fraud detection specialist.
    Analyze the claim and transaction history to detect fraud patterns.
    
    Look for:
    - Unknown merchant names
    - Unusual transaction amounts
    - Transaction location mismatches
    - Multiple disputes from same customer
    - Transactions at odd hours
    
    Respond ONLY with valid JSON:
    {{
        "fraud_score": 0.0 to 1.0,
        "risk_level": "low / medium / high",
        "fraud_indicators": ["list of detected indicators"],
        "recommendation": "approve / investigate / reject"
    }}
    """),
    ("human", """
    Claim: {claim}
    Transaction history: {transaction_history}
    """)
])

fraud_chain = fraud_prompt | llm | JsonOutputParser()


def run_fraud_detection(claim: dict) -> dict:
    # Mock transaction history — replace with real DB query later
    transaction_history = """
    2024-01-15  Amazon          $35.00   - normal
    2024-01-28  Shell Gas       $55.00   - normal
    2024-02-10  Netflix         $15.99   - normal
    2024-02-20  Walmart         $89.00   - normal
    2024-03-05  UNKNOWN-MERCH-X $499.00  - disputed
    """

    return fraud_chain.invoke({
        "claim": str(claim),
        "transaction_history": transaction_history
    })