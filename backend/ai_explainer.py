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

        prompt = f"""You are a blockchain security expert teaching a beginner developer.
A smart contract scan found these security issues:
{vuln_text}

For each issue explain:
1. What is this vulnerability in simple English
2. How a hacker could exploit it step by step
3. Exact code fix with before and after example

Be clear, simple and educational."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI explanation error: {str(e)}"