import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()

# 1. Structured output schema
class DisputeClaim(BaseModel):
    customer_id: str
    transaction_id: str
    disputed_amount: float
    dispute_type: str        # unauthorized | duplicate | merchant_error | other
    transaction_date: str
    merchant_name: str
    customer_description: str
    missing_fields: List[str]
    confidence_score: float

# 2. LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# 3. Prompt
intake_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a banking dispute intake specialist.
    Extract structured information from the customer's dispute message.
    
    Fields to extract:
    - customer_id, transaction_id, disputed_amount
    - dispute_type (unauthorized / duplicate / merchant_error / other)
    - transaction_date, merchant_name
    - customer_description (clean 1-2 sentence summary)
    - missing_fields (list any fields not found)
    - confidence_score (0.0 to 1.0)
    
    Respond ONLY with valid JSON. No extra text.
    """),
    ("human", "{customer_input}")
])

# 4. Chain
intake_chain = intake_prompt | llm | JsonOutputParser()


def run_intake(customer_input: str) -> dict:
    return intake_chain.invoke({"customer_input": customer_input})