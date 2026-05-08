import { useState } from "react";
import axios from "axios";

export default function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const submitDispute = async () => {
    console.log("SUBMIT FUNCTION CALLED");
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.post("https://claimant-api.blueocean-104587c3.canadacentral.azurecontainerapps.io/dispute", {
        raw_input: input
      });
      setResult(response.data);
    } catch (err) {
      // alert("Error submitting dispute. Is the backend running?");
      console.error("Full error:", err);
      alert("Error: " + (err.response?.data?.detail || err.message || JSON.stringify(err)));
    }
    setLoading(false);
  };

  const getDecisionColor = (decision) => {
    if (decision === "approve") return "#16a34a";
    if (decision === "reject") return "#dc2626";
    return "#d97706";
  };

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", padding: "0 20px", fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 4 }}>Claimant</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Banking Dispute Portal</p>

      {/* Input */}
      <div style={{ marginBottom: 16 }}>
        <label style={{ fontWeight: 600, display: "block", marginBottom: 8 }}>
          Describe your dispute
        </label>
        <textarea
          rows={5}
          style={{ width: "100%", padding: 12, border: "1px solid #d1d5db", borderRadius: 8, fontSize: 14 }}
          placeholder="e.g. On March 5th 2024 I noticed a charge of $499 from UNKNOWN-MERCH-X on my account ending in 4521. Customer ID is CUST-8821, transaction ID is TXN-20240305-499. I never made this purchase."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </div>

      <button
        type="button"
        onClick={submitDispute}
        disabled={loading || !input}
        style={{
          background: "#2563eb", color: "white", padding: "10px 24px",
          border: "none", borderRadius: 8, fontWeight: 600,
          cursor: loading ? "not-allowed" : "pointer", opacity: loading ? 0.7 : 1
        }}
      >
        {loading ? "Processing..." : "Submit Dispute"}
      </button>

      {/* Results */}
      {result && (
        <div style={{ marginTop: 32 }}>

          {/* Decision Banner */}
          <div style={{
            background: getDecisionColor(result.decision),
            color: "white", padding: "16px 20px",
            borderRadius: 8, marginBottom: 16
          }}>
            <div style={{ fontSize: 12, textTransform: "uppercase", opacity: 0.85 }}>Decision</div>
            <div style={{ fontSize: 24, fontWeight: 700, textTransform: "capitalize" }}>{result.decision}</div>
            <div style={{ fontSize: 14, marginTop: 4, opacity: 0.9 }}>{result.reason}</div>
          </div>

          {/* Claim Details */}
          <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 16 }}>
            <h3 style={{ fontWeight: 600, marginBottom: 12 }}>Claim Details</h3>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, fontSize: 14 }}>
              <div><span style={{ color: "#6b7280" }}>Customer ID:</span> {result.claim.customer_id}</div>
              <div><span style={{ color: "#6b7280" }}>Transaction ID:</span> {result.claim.transaction_id}</div>
              <div><span style={{ color: "#6b7280" }}>Amount:</span> ${result.claim.disputed_amount}</div>
              <div><span style={{ color: "#6b7280" }}>Merchant:</span> {result.claim.merchant_name}</div>
              <div><span style={{ color: "#6b7280" }}>Date:</span> {result.claim.transaction_date}</div>
              <div><span style={{ color: "#6b7280" }}>Type:</span> {result.claim.dispute_type}</div>
            </div>
          </div>

          {/* Fraud Score */}
          <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 16 }}>
            <h3 style={{ fontWeight: 600, marginBottom: 8 }}>Fraud Score</h3>
            <div style={{ background: "#f3f4f6", borderRadius: 999, height: 12, overflow: "hidden" }}>
              <div style={{
                background: result.fraud_score > 0.7 ? "#dc2626" : result.fraud_score > 0.4 ? "#d97706" : "#16a34a",
                width: `${result.fraud_score * 100}%`, height: "100%", borderRadius: 999
              }}/>
            </div>
            <div style={{ fontSize: 13, color: "#6b7280", marginTop: 4 }}>
              {(result.fraud_score * 100).toFixed(0)}% risk
            </div>
          </div>

          {/* Customer Message */}
          <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 16 }}>
            <h3 style={{ fontWeight: 600, marginBottom: 8 }}>Customer Notification</h3>
            <p style={{ fontSize: 14, color: "#374151", lineHeight: 1.6 }}>{result.customer_message}</p>
          </div>

          {/* Escalation Summary */}
          {result.escalation_summary && (
            <div style={{ border: "1px solid #fbbf24", background: "#fffbeb", borderRadius: 8, padding: 16 }}>
              <h3 style={{ fontWeight: 600, marginBottom: 8 }}>Escalation Summary</h3>
              <p style={{ fontSize: 14, color: "#374151", lineHeight: 1.6 }}>{result.escalation_summary}</p>
            </div>
          )}

        </div>
      )}
    </div>
  );
}