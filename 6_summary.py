from typing import List, TypedDict
from langgraph.graph import END, START, StateGraph


# 1. Define State
class EvaluationState(TypedDict):
    individual_scores: List[float]
    avg_score: float
    status: str
    summary: str


# 2. Define Node Logic (Pure Python)
def calculate_metrics(state: EvaluationState):
    scores = state["individual_scores"]
    avg = sum(scores) / len(scores) if scores else 0.0

    return {
        "avg_score": round(avg, 2),
        "status": "PASS" if avg >= 60 else "FAIL",
    }


def generate_summary(state: EvaluationState):
    summary_text = (
        f"Evaluation Complete | Average Score: {state['avg_score']}% "
        f"| Final Result: {state['status']}"
    )
    return {"summary": summary_text}


# 3. Build Graph
builder = StateGraph(EvaluationState)

builder.add_node("calculate", calculate_metrics)
builder.add_node("summarize", generate_summary)

builder.add_edge(START, "calculate")
builder.add_edge("calculate", "summarize")
builder.add_edge("summarize", END)

workflow = builder.compile()

# 4. Test Execution
if __name__ == "__main__":
    result = workflow.invoke({"individual_scores": [85, 72, 90, 68]})
    print(result)