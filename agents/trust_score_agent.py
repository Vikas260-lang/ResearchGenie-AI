from pydantic import BaseModel


class TrustScoreOutput(BaseModel):
    trust_score: float
    confidence_level: str
    explanation: str


# ---------------- FIXED FUNCTIONS ----------------

def compute_evidence_score(evidence):
    if not evidence:
        return 0.4
    return min(0.6 + (len(evidence) * 0.1), 1.0)


def compute_debate_score(verdicts):
    mapping = {
        "supported": 1.0,
        "partially_supported": 0.6,
        "rejected": 0.2,
        "not supported": 0.2
    }

    scores = []

    for v in verdicts:

        # ✅ CASE 1: dict format
        if isinstance(v, dict):
            if "confidence_score" in v:
                scores.append(v.get("confidence_score", 50) / 100)
            else:
                scores.append(mapping.get(v.get("verdict", ""), 0.5))

        # ✅ CASE 2: object (just in case)
        else:
            try:
                scores.append(getattr(v, "confidence_score", 50) / 100)
            except:
                scores.append(0.5)

    return sum(scores) / len(scores) if scores else 0.5


def compute_contradiction_penalty(anomalies):
    if not anomalies:
        return 0
    
    return min(len(anomalies) * 0.1, 0.5)


def compute_plagiarism_penalty(plagiarism_score):
    return plagiarism_score * 0.2


# ---------------- MAIN ----------------

def run_trust_score(evidence, verdicts, anomalies, plagiarism_score):
    
    evidence_score = compute_evidence_score(evidence)
    debate_score = compute_debate_score(verdicts)
    contradiction_penalty = compute_contradiction_penalty(anomalies)
    plagiarism_penalty = compute_plagiarism_penalty(plagiarism_score)

    trust_score = (
        (0.4 * evidence_score) +
        (0.4 * debate_score) -
        contradiction_penalty -
        plagiarism_penalty
    )

    trust_score = max(0, min(trust_score, 1))

    if trust_score > 0.75:
        level = "High"
    elif trust_score > 0.5:
        level = "Moderate"
    else:
        level = "Low"

    explanation = f"""
    Evidence strength: {round(evidence_score,2)}
    Debate support: {round(debate_score,2)}
    Contradictions penalty: {round(contradiction_penalty,2)}
    Plagiarism penalty: {round(plagiarism_penalty,2)}
    """

    return TrustScoreOutput(
        trust_score=round(trust_score, 2),
        confidence_level=level,
        explanation=explanation.strip()
    )

if __name__ == "__main__":
    from knowledge_agent import run_knowledge
    from synthesis_agent import run_synthesis
    from plagiarism_agent import run_plagiarism

    task = "Evaluate EV charging infrastructure in India"

    # STEP 1: Knowledge (includes debate)
    knowledge = run_knowledge(task)

    evidence = [e.model_dump() for e in knowledge.evidence]
    claims = [c.model_dump() for c in knowledge.claims]
    debates = [d.model_dump() for d in knowledge.debates]
    verdicts = [v.model_dump() for v in knowledge.verdicts]

    # STEP 2: Synthesis
    final_answer = run_synthesis(
        claims=claims,
        debates=debates,
        verdicts=verdicts,
        evidence=evidence
    )

    # STEP 3: Plagiarism
    plagiarism_score = run_plagiarism(
        report=final_answer,
        evidence=evidence
    )

    # STEP 4: Trust Score
    trust = run_trust_score(
        evidence=evidence,
        verdicts=verdicts,
        anomalies=[],  # not used now
        plagiarism_score=plagiarism_score
    )

    print("\nTRUST SCORE:\n")
    print(trust.model_dump())