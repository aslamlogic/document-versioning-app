import httpx, os, json
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
VALIDATOR_MODEL = "meta-llama/llama-3-70b-instruct"
async def run_validator(previous: str, changes: str, applied: str):
    prompt = f"Verify all changes applied exactly.\nPrevious: {previous}\nChanges: {changes}\nApplied: {applied}\nReturn JSON: {{'approved': bool, 'discrepancies': list[str], 'report': str}}"
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}, json={"model": VALIDATOR_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}, timeout=60)
        if resp.status_code == 200:
            try: return json.loads(resp.json()["choices"][0]["message"]["content"])
            except: return {"approved": False, "discrepancies": ["Parse error"], "report": ""}
        return {"approved": False, "discrepancies": [f"API error {resp.status_code}"], "report": ""}
