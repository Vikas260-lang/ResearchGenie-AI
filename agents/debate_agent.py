from pydantic import BaseModel
from typing import List
import requests
import json


# ---------------- MODELS ----------------
class Argument(BaseModel):
    side: str  # "pro" or "con"
    reasoning: str
    evidence_ids: List[str]


class Debate(BaseModel):
    claim_id: str
    arguments: List[Argument]


class Verdict(BaseModel):
    claim_id: str
    verdict: str  # supported / partially_supported / rejected
    confidence_score: float
    justification: str


class DebateOutput(BaseModel):
    debates: List[Debate]
    verdicts: List[Verdict]


# ---------------- PROMPT ----------------
DEBATE_PROMPT = """
You are an expert AI research analyst.

Given the following claims and evidence:

CLAIMS:
{claims}

EVIDENCE:
{evidence}

For EACH claim:

- You MUST generate:
  1. At least ONE PRO argument
  2. At least ONE CON argument (even if weak or hypothetical)

- If no strong counterargument exists:
  → create a logical limitation, assumption, or potential risk

- DO NOT skip CON arguments under any condition

Each claim MUST contain BOTH:
- one "pro" argument
- one "con" argument

Return STRICT JSON in this format:

{{
  "debates": [
    {{
      "claim_id": "string",
      "arguments": [
        {{
          "side": "pro",
          "reasoning": "text",
          "evidence_ids": ["id1", "id2"]
        }},
        {{
          "side": "con",
          "reasoning": "text",
          "evidence_ids": ["id3"]
        }}
      ]
    }}
  ],
  "verdicts": [
    {{
      "claim_id": "string",
      "verdict": "supported",
      "confidence_score": 85,
      "justification": "text"
    }}
  ]
}}
"""


# ---------------- LLM CALL ----------------
def call_llm(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise ValueError(f"Ollama error: {response.text}")

    data = response.json()

    if "response" not in data:
        raise ValueError(f"Unexpected Ollama output: {data}")

    return data["response"]


# ---------------- JSON EXTRACTOR ----------------
def extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError("No JSON found")

    candidate = text[start:end]

    try:
        json.loads(candidate)
        return candidate
    except Exception as e:
        raise ValueError(f"Invalid JSON: {e}")


# ---------------- CLEAN JSON ----------------
def clean_json(text: str) -> str:
    text = text.replace("’", "'")
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    return text


# ---------------- 🔥 FORCE PRO + CON ----------------
def enforce_pro_con(parsed_json):
    for debate in parsed_json.get("debates", []):
        arguments = debate.get("arguments", [])

        has_pro = any(arg.get("side") == "pro" for arg in arguments)
        has_con = any(arg.get("side") == "con" for arg in arguments)

        # Add missing PRO
        if not has_pro:
            arguments.append({
                "side": "pro",
                "reasoning": "Supporting evidence suggests the claim is valid.",
                "evidence_ids": []
            })

        # Add missing CON
        if not has_con:
            arguments.append({
                "side": "con",
                "reasoning": "Potential limitations or edge cases may affect this claim.",
                "evidence_ids": []
            })

        debate["arguments"] = arguments

    return parsed_json


# ---------------- MAIN FUNCTION ----------------
def run_debate(claims: list, evidence: list) -> DebateOutput:

    prompt = DEBATE_PROMPT.format(
        claims=json.dumps(claims, indent=2),
        evidence=json.dumps(evidence, indent=2)
    )

    raw_output = call_llm(prompt)

    print("\n===== RAW OUTPUT =====\n", raw_output)

    try:
        clean_output = extract_json(raw_output)
        clean_output = clean_json(clean_output)

        parsed = json.loads(clean_output)

        # 🔥 APPLY FIX HERE
        parsed = enforce_pro_con(parsed)

        validated = DebateOutput(**parsed)

        return validated

    except Exception as e:
        raise ValueError(f"Debate output invalid: {e}\nRaw Output: {raw_output}")


# ---------------- TEST RUN ----------------
if __name__ == "__main__":
    from research_agent import run_research
    from extraction_agent import run_extraction

    task = "Evaluate charging infrastructure availability in India"

    research_result = run_research(task)

    extraction_result = run_extraction(
        evidence=[e.model_dump() for e in research_result.evidence]
    )

    debate_result = run_debate(
        claims=[c.model_dump() for c in extraction_result.claims],
        evidence=[e.model_dump() for e in research_result.evidence]
    )

    print("\n===== FINAL OUTPUT =====\n")
    print(json.dumps(debate_result.model_dump(), indent=2))