from db.database import get_connection

def save_claim(result: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO claims (
            customer_id, transaction_id, disputed_amount,
            dispute_type, transaction_date, merchant_name,
            customer_description, confidence_score,
            verified, fraud_score, decision,
            refund_amount, decision_reason,
            customer_message, escalation_summary
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (transaction_id) DO UPDATE SET
            decision = EXCLUDED.decision,
            fraud_score = EXCLUDED.fraud_score
    """, (
        result["claim"]["customer_id"],
        result["claim"]["transaction_id"],
        result["claim"]["disputed_amount"],
        result["claim"]["dispute_type"],
        result["claim"]["transaction_date"],
        result["claim"]["merchant_name"],
        result["claim"]["customer_description"],
        result["claim"]["confidence_score"],
        result["verified"],
        result["fraud_score"],
        result["decision"],
        result["refund_amount"],
        result["decision_reason"],
        result["customer_message"],
        result["escalation_summary"]
    ))

    conn.commit()
    cur.close()
    conn.close()

def get_all_claims():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM claims ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows