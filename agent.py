import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class BusinessAnalystAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("GEMINI_API_KEY not found in environment")

        genai.configure(api_key=api_key)

        # Use best available model
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")

    def analyze(self, url: str, brd: str):
        time.sleep(2)  # prevent hitting rate limit

        prompt = self._build_prompt(url, brd)
        response = self.model.generate_content(prompt)

        return self._parse_response(response.text)

    def _build_prompt(self, url, brd):
        return f"""
You are a SENIOR BUSINESS ANALYST + QA EXPERT.

Your job is NOT just summarizing.
You must deeply understand the system like a HUMAN TESTER.

INPUT:
Website/App URL: {url}
BRD / Documentation:
{brd}

---

GOAL:
Before testing, prove you understand the system perfectly.

Return STRICT JSON in this format:

{{
  "system_purpose": "...",
  "user_personas": ["...", "..."],
  "critical_business_paths": ["...", "..."],
  "assumed_logic": ["...", "..."]
}}

---

THINK LIKE:
- QA Engineer
- Business Analyst
- Product Owner

---

INSTRUCTIONS:

1. SYSTEM PURPOSE
- What problem does this system solve?
- What is its business goal?

2. USER PERSONAS
- Who are the users?
- (Admin, User, Visitor, etc.)

3. CRITICAL BUSINESS PATHS (VERY IMPORTANT)
- End-to-end flows that MUST work
- Example:
  - Signup → Login → Dashboard
  - Create → Update → Delete flows

4. ASSUMED LOGIC (MOST IMPORTANT)
- Write logic assumptions like:
  "If user signup is interrupted, system should allow resume"
  "Passwords should never be visible"
  "Duplicate entries should be prevented"

- These will later become TEST CASES

---

IMPORTANT:
- Think deeply (edge cases, UX, logic gaps)
- Be specific
- Do NOT give explanation outside JSON
"""

    def _parse_response(self, text):
        """
        Basic parser (safe fallback if model returns extra text)
        """
        import json

        try:
            # Try direct JSON
            return json.loads(text)
        except:
            # Extract JSON manually
            start = text.find("{")
            end = text.rfind("}") + 1
            json_str = text[start:end]

            return json.loads(json_str)