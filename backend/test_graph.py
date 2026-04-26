from graph.claim_graph import build_graph

graph = build_graph()

result = graph.invoke({
    "raw_input": """
    Hi, I'd like to dispute a charge on my account.
    On March 5th 2024 I noticed a charge of $499 from UNKNOWN-MERCH-X 
    on my account ending in 4521. Customer ID is CUST-8821, 
    transaction ID is TXN-20240305-499. I never made this purchase.
    """,
    "claim": {},
    "verified": False,
    "fraud_score": 0.0,
    "fraud_recommendation": "",
    "decision": "",
    "refund_amount": 0.0,
    "decision_reason": ""
})

print("\nFinal Decision:", result["decision"])
print("Reason:", result["decision_reason"])
print("Refund Amount:", result["refund_amount"])