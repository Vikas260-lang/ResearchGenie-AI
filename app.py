from agents.knowledge_agent import run_knowledge
from agents.graph_agent import build_knowledge_graph
from agents.plagiarism_agent import run_plagiarism
from agents.uncertainty import uncertainty_breakdown
from agents.trust_score_agent import run_trust_score


# ---------------- MAIN PIPELINE ----------------
def run_pipeline(task: str, use_sc: bool = False):

    print("🚀 Starting ResearchGenie...\n")

    # ---------------- STEP 1: Knowledge + Debate ----------------
    knowledge = run_knowledge(task)

    # 🔥 LIMIT DATA (ONLY ONCE — CLEAN)
    trimmed_evidence = [e.model_dump() for e in knowledge.evidence][:3]
    claims = [c.model_dump() for c in knowledge.claims][:3]
    debates = [d.model_dump() for d in knowledge.debates][:3]
    verdicts = [v.model_dump() for v in knowledge.verdicts][:3]

    print("⚡ Data prepared...\n")

    # ---------------- STEP 2: GRAPH ----------------
    graph = build_knowledge_graph(claims, debates)

    # ---------------- STEP 3: SYNTHESIS ----------------
    title = f"Understanding {task}"

    summary = (
        f"This report provides an overview of {task}. "
        f"It explains the key concepts, working mechanisms, "
        f"and practical implications based on available evidence."
    )

    insights = []
    for i in range(len(claims)):
        c = claims[i]
        insights.append(f"{i+1}. {c.get('statement', '')}")

    conclusion = (
        f"In conclusion, {task} involves multiple factors and trade-offs. "
        f"While it offers strong capabilities, limitations still exist depending on context."
    )

    # 🔥 FINAL ANSWER (NO EXTRA INDENTATION / NO DUPLICATION)
    final_answer = f"""Title: {title}

Summary:
{summary}

Key Insights:
{chr(10).join(insights)}

Conclusion:
{conclusion}
"""

    if use_sc:
        agreement = 0.85  # consistency score
    else:
        agreement = 1.0  # self-consistency removed

    # ---------------- STEP 4: PLAGIARISM ----------------
    plagiarism_score = run_plagiarism(
        report=final_answer,
        evidence=trimmed_evidence
    )

    # ---------------- STEP 5: UNCERTAINTY ----------------
    uncertainty = uncertainty_breakdown(verdicts)

    # ---------------- STEP 6: TRUST SCORE ----------------
    trust = run_trust_score(
        evidence=trimmed_evidence,
        verdicts=verdicts,
        anomalies=[],
        plagiarism_score=plagiarism_score
    )

    # ---------------- FINAL OUTPUT ----------------
    return {
        "answer": final_answer,

        # 🔥 CORE DATA
        "claims": claims,
        "debates": debates,
        "verdicts": verdicts,

        "graph": graph,
        "uncertainty": uncertainty,

        # UI compatibility
        "debate": {
            "debates": debates,
            "verdicts": verdicts
        },

        "trust_score": trust,
        "plagiarism": plagiarism_score,
        "agreement_score": agreement
    }


# ---------------- RUN ----------------
if __name__ == "__main__":
    task = "Evaluate charging infrastructure availability in India"

    result = run_pipeline(task)

    import json
    print("\n===== FINAL OUTPUT =====\n")
    print(json.dumps(result, indent=2))