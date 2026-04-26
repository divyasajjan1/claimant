from agents.intake_agent import run_intake

test_input = """
Hi, I'd like to dispute a charge on my account.
On March 5th I noticed a charge of $499 from a merchant 
called UNKNOWN-MERCH-X on my account ending in 4521. 
My customer ID is CUST-8821 and the transaction ID is 
TXN-20240305-499. I never made this purchase.
"""

result = run_intake(test_input)
print(result)