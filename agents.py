from typing import Dict, Any
from tools import extract_numbers, short_summary

# This module contains a deterministic "agent" that formats analysis results
# as JSON without calling any external LLM. It simulates what a well-crafted
# prompt + LLM would produce, so tests can validate outputs deterministically.

def analyze_text_deterministic(text: str) -> Dict[str,Any]:
    summary = short_summary(text, max_sentences=2)
    numbers = extract_numbers(text)
    # pick top numeric mentions heuristically
    totals = sorted(set(numbers), key=lambda x: (-len(x), x))[:8]
    currency_mentions = [c for c in ["USD","INR","EUR","GBP","$","₹"] if c in text]
    risks = []
    if "loss" in text.lower() or "losses" in text.lower():
        risks.append("Reported losses or negative net income mentioned in document.")
    if "debt" in text.lower():
        risks.append("Debt exposure mentioned; review leverage and maturities.")
    recommendations = [
        "Validate numeric totals against source tables.",
        "Confirm currency and time period for all figures.",
    ]
    return {
        "summary": summary,
        "key_facts": {
            "totals": totals,
            "currency_mentions": currency_mentions,
            "numeric_mentions_count": len(numbers)
        },
        "risks": risks,
        "recommendations": recommendations
    }
