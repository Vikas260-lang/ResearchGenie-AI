def uncertainty_breakdown(verdicts):
    result = []

    for v in verdicts:

        # ✅ handle dict safely
        if isinstance(v, dict):
            score = v.get("confidence_score", 50)
            claim_id = v.get("claim_id", "Unknown")

        # ✅ fallback (if object ever comes)
        else:
            score = getattr(v, "confidence_score", 50)
            claim_id = getattr(v, "claim_id", "Unknown")

        if score > 80:
            level = "High Confidence"
        elif score > 60:
            level = "Moderate"
        else:
            level = "Low / Uncertain"

        result.append({
            "claim_id": claim_id,
            "confidence": score,
            "level": level
        })

    return result