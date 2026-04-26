import os
import pdfplumber
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

verify_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a bank document verification specialist.
    You will receive a disputed transaction claim and a bank statement text.
    
    Your job:
    - Check if the disputed transaction exists in the statement
    - Verify the amount matches
    - Verify the merchant name matches
    - Verify the date matches
    
    Respond ONLY with valid JSON:
    {{
        "transaction_found": true/false,
        "amount_matches": true/false,
        "merchant_matches": true/false,
        "date_matches": true/false,
        "verified": true/false,
        "notes": "brief explanation"
    }}
    """),
    ("human", """
    Claim details: {claim}
    Bank statement: {statement}
    """)
])

verify_chain = verify_prompt | llm | JsonOutputParser()


def extract_text_from_pdf(file_path: str) -> str:
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages)


def run_doc_verify(claim: dict, file_path: str = "") -> dict:
    # If no document uploaded, use mock statement
    if file_path:
        statement = extract_text_from_pdf(file_path)
    else:
        statement = """
        Account: ****4521 - Customer: CUST-8821
        Date        Merchant            Amount
        2024-03-01  Amazon              $49.99
        2024-03-03  Shell Gas           $60.00
        2024-03-05  UNKNOWN-MERCH-X     $499.00
        2024-03-07  Walmart             $120.00
        """

    return verify_chain.invoke({
        "claim": str(claim),
        "statement": statement
    })