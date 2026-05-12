from pydantic import BaseModel
from typing import List
import requests
import json

# ---------------- MODELS ----------------
class Insight(BaseModel):
    insight: str


class FinalReport(BaseModel):
    title: str
    summary: str
    key_insights: List[Insight]
    conclusion: str


# ---------------- PROMPT ----------------
SYNTHESIS_PROMPT = """
You are a Synthesis Agent.

Your job:
- Combine all previous outputs into a final research report

STRICT RULES:
- Output ONLY valid JSON
-Maximum 120–150 words
-Focus on key insights only
-Be concise and direct

FORMAT:
{{
  "title": "",
  "summary": "",
  "key_insights": [
    {{"insight": ""}}
  ],
  "conclusion": ""
}}

INPUT DATA:

EVIDENCE:
{evidence}

CLAIMS:
{claims}

DEBATES:
{debates}

VERDICTS:
{verdicts}
"""


# ---------------- LLM ----------------
def call_llm(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
    "model": "mistral",
    "prompt": prompt,
    "stream": False,
    "options": {
        "num_predict": 80,
        "temperature": 0.3,
        "top_p": 0.9
    }
}

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise ValueError(f"Ollama error: {response.text}")

    return response.json()["response"]


# ---------------- JSON EXTRACT ----------------
def extract_json(text: str):
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError("No JSON found")

    return json.loads(text[start:end])


# ---------------- MAIN FUNCTION ----------------
def run_synthesis(claims, debates, verdicts, evidence) -> str:

    prompt = SYNTHESIS_PROMPT.format(
        evidence=json.dumps(evidence, indent=2),
        claims=json.dumps(claims, indent=2),
        debates=json.dumps(debates, indent=2),
        verdicts=json.dumps(verdicts, indent=2),
    )

    raw_output = call_llm(prompt)

    print("RAW OUTPUT:\n", raw_output)

    try:
        parsed = extract_json(raw_output)
        report = FinalReport(**parsed)

        # ✅ Convert to readable text for UI
        formatted = f"""
### {report.title}

{report.summary}

#### Key Insights:
"""
        for ins in report.key_insights:
            formatted += f"- {ins.insight}\n"

        formatted += f"\n### Conclusion\n{report.conclusion}"

        return formatted

    except Exception:
        # 🔥 fallback
        return raw_output[:800]