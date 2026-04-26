from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.intake_agent import run_intake
from agents.doc_verify_agent import run_doc_verify
from agents.fraud_agent import run_fraud_detection
from agents.approval_agent import run_approval
from agents.comms_agent import run_comms
from agents.escalation_agent import run_escalation

class ClaimState(TypedDict):
    raw_input: str
    claim: dict
    verified: bool
    fraud_score: float
    fraud_recommendation: str
    decision: str
    refund_amount: float
    decision_reason: str
    customer_message: str
    escalation_summary: str

def intake_node(state: ClaimState) -> ClaimState:
    state["claim"] = run_intake(state["raw_input"])
    return state

def doc_verify_node(state: ClaimState) -> ClaimState:
    result = run_doc_verify(state["claim"])
    state["verified"] = result["verified"]
    print("Doc Verify:", result)
    return state

def fraud_node(state: ClaimState) -> ClaimState:
    result = run_fraud_detection(state["claim"])
    state["fraud_score"] = result["fraud_score"]
    state["fraud_recommendation"] = result["recommendation"]
    print("Fraud Detection:", result)
    return state

def approval_node(state: ClaimState) -> ClaimState:
    result = run_approval(
        state["claim"],
        state["verified"],
        state["fraud_score"],
        state["fraud_recommendation"]
    )
    state["decision"] = result["decision"]
    state["refund_amount"] = result["refund_amount"]
    state["decision_reason"] = result["reason"]
    print("Approval:", result)
    return state

def comms_node(state: ClaimState) -> ClaimState:
    result = run_comms(state["claim"], state["decision"], state["decision_reason"])
    state["customer_message"] = result["message"]
    print("Comms:", result)
    return state

def escalation_node(state: ClaimState) -> ClaimState:
    result = run_escalation(
        state["claim"],
        state["verified"],
        state["fraud_score"],
        state["decision_reason"]
    )
    state["escalation_summary"] = result["summary"]
    print("Escalation:", result)
    return state

# Conditional routing after approval
def route_after_approval(state: ClaimState) -> str:
    if state["decision"] == "escalate":
        return "escalation"
    return "comms"

def build_graph():
    graph = StateGraph(ClaimState)

    graph.add_node("intake", intake_node)
    graph.add_node("doc_verify", doc_verify_node)
    graph.add_node("fraud_detection", fraud_node)
    graph.add_node("approval", approval_node)
    graph.add_node("comms", comms_node)
    graph.add_node("escalation", escalation_node)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "doc_verify")
    graph.add_edge("doc_verify", "fraud_detection")
    graph.add_edge("fraud_detection", "approval")

    # Conditional edge — escalate or notify customer
    graph.add_conditional_edges("approval", route_after_approval, {
        "escalation": "escalation",
        "comms": "comms"
    })

    graph.add_edge("escalation", "comms")  # always notify customer after escalation
    graph.add_edge("comms", END)

    return graph.compile()