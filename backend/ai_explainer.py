from groq import Groq
import os

def explain_vulnerability(vulnerabilities):
    if not vulnerabilities:
        return "✅ No vulnerabilities found! Your contract looks safe."

    api_key = os.environ.get('GROQ_API_KEY')

    if not api_key:
        return "❌ GROQ_API_KEY not set in environment."

    try:
        client = Groq(api_key=api_key)

        vuln_text = ""
        for v in vulnerabilities:
            vuln_text += f"\n- Issue: {v['name']}\n- Severity: {v['severity']}\n- Description: {v['description']}\n"

        prompt = f"""You are a blockchain security expert. Analyze these smart contract vulnerabilities:
{vuln_text}

For each vulnerability respond in this EXACT format with no markdown symbols like # or **:

VULNERABILITY: [name in caps]
WHAT IT IS: [1 sentence simple explanation]
HOW HACKERS EXPLOIT IT: [2-3 short bullet points starting with ->]
CODE FIX: [1-2 sentence fix]
---

Keep it short, clear and professional. No markdown. No hashtags. No asterisks."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI explanation error: {str(e)}"