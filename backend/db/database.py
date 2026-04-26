import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        sslmode="require"        # Azure requires SSL
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id SERIAL PRIMARY KEY,
            customer_id VARCHAR(50),
            transaction_id VARCHAR(50) UNIQUE,
            disputed_amount NUMERIC,
            dispute_type VARCHAR(50),
            transaction_date DATE,
            merchant_name VARCHAR(100),
            customer_description TEXT,
            confidence_score NUMERIC,
            verified BOOLEAN,
            fraud_score NUMERIC,
            decision VARCHAR(20),
            refund_amount NUMERIC,
            decision_reason TEXT,
            customer_message TEXT,
            escalation_summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully")

if __name__ == "__main__":
    init_db()