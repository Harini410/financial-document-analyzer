import os
import json
import time
import requests

CREWAI_API_KEY = os.getenv('CREWAI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def do_post_with_retries(url, headers, payload, retries=3, backoff=1.0):
    last_exc = None
    for i in range(retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            try:
                return resp.json()
            except:
                return {'text': resp.text}
        except Exception as e:
            last_exc = e
            time.sleep(backoff * (2 ** i))
    raise last_exc

def call_llm(prompt: str, max_tokens: int = 512, temperature: float = 0.0):
    if not CREWAI_API_KEY and not OPENAI_API_KEY:
        return {
            "text": json.dumps({
                "document_type": "balance_sheet",
                "summary": "Deterministic summary (offline mode)",
                "key_facts": {"total_assets": "100000", "total_liabilities": "40000"},
                "risks": ["related_party_transactions"],
                "recommendations": ["review_related_party_notes"]
            })
        }
    if CREWAI_API_KEY:
        url = os.getenv('CREWAI_API_URL', 'https://api.crew.ai/v1/generate')
        headers = {'Authorization': f'Bearer {CREWAI_API_KEY}', 'Content-Type': 'application/json'}
        payload = {'prompt': prompt, 'max_tokens': max_tokens, 'temperature': temperature}
        return do_post_with_retries(url, headers, payload)
    if OPENAI_API_KEY:
        url = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1/chat/completions')
        headers = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'}
        payload = {
            'model': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            'messages': [{'role': 'system', 'content': 'You are a financial document analyzer.'},
                         {'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens,
            'temperature': temperature
        }
        return do_post_with_retries(url, headers, payload)
    raise RuntimeError('No LLM configured and deterministic fallback disabled.')
