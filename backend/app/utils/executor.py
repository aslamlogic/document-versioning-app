import httpx, os, json
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
EXECUTOR_MODEL = "mistralai/mixtral-8x7b-instruct"
async def run_executor(previous_content: str, changes_content: str, instructions: str = ""):
    prompt = f"Apply changes verbatim.\nPrevious: {previous_content}\nChanges: {changes_content}\nInstructions: {instructions}\nReturn JSON: {{'success': bool, 'applied_content': str, 'changes_summary': str}}"
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}, json={"model": EXECUTOR_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}, timeout=60)
        if resp.status_code == 200:
            try: return json.loads(resp.json()["choices"][0]["message"]["content"])
            except: return {"success": False, "applied_content": "", "changes_summary": "Parse error"}
        return {"success": False, "applied_content": "", "changes_summary": f"API error {resp.status_code}"}
