# backend/smart_comments/classifier.py
import re
from typing import Literal
from openai import OpenAI
from django.conf import settings
import openai

# Create an OpenAI client using your API key from settings
openai.api_key = settings.OPENAI_API_KEY
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# === 1. Known dangerous patterns (SQLi, XSS, Shell, Traversal) ===
DANGEROUS_PATTERNS = [
    r'(?i)union.*select.*from',           # SQL Injection
    r'(?i)drop\s+table',                  # DROP TABLE
    r'(?i)insert.*into',                  # INSERT attempts
    r'(?i)delete.*from',                  # DELETE FROM
    r'(?i)update.*set',                   # UPDATE SET
    r'(?i)or\s+1\s*=\s*1',                # Classic login bypass
    r'(?i)--\s',                          # SQL comment
    r'<script\b',                         # XSS: <script>
    r'javascript:',                       # javascript: URLs
    r'onload\s*=', r'onclick\s*=',        # Event handlers
    r'<\s*iframe', r'<\s*img.*src\s*=',   # iframe / img src attacks
    r'\.\./', r'\.\.\\',                  # Path traversal
    r';.*(rm\s|del\s|shutdown|reboot)',  # Shell commands
    r'base64\s*,',                        # Data URIs with base64
    r'&#x?[0-9a-f]+;',                    # HTML entities abuse
]

# === 2. Repetitive spam / DoS patterns ===
REPEAT_CHAR_THRESHOLD = 15      # "AAAAAAA..." spam
MAX_LENGTH = 2000               # Block huge payloads
MIN_WORDS = 3
MIN_LENGTH = 12

# === 3. Suspicious Unicode / homoglyphs ===
UNICODE_SUSPICIOUS = r'[\u200B-\u200D\u202A-\u202E\u2066-\u2069\uFEFF]'  # Zero-width, RTL, etc.


def manual_checks(text: str) -> Literal["safe", "needs_review"]:
    """
    Returns 'safe', 'needs_review', blocked
    """
    if not text or not isinstance(text, str):
        return "needs_review"

    # --- 1. Block massive payloads (DoS protection) ---
    if len(text) > MAX_LENGTH:
        return "needs_review"

    # --- 2. Check for dangerous patterns (SQLi, XSS, Shell, etc.) ---
    text_lower = text.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, text_lower):
            print("→ BLOCKED: DB-dangerous pattern detected.\n")
            return "blocked"

    # --- 3. Detect encoded attacks ---
    if re.search(r'data:text/html', text_lower) or \
       re.search(r'base64[^,]*,', text_lower):
        return "needs_review"

    # --- 4. Unicode abuse / invisible chars ---
    if re.search(UNICODE_SUSPICIOUS, text):
        return "needs_review"

    # --- 5. Repetitive characters (spam / DoS) ---
    if re.search(r'(.)\1{%d,}' % REPEAT_CHAR_THRESHOLD, text):
        return "needs_review"

    # --- 6. Too short or meaningless ---
    if len(text) < MIN_LENGTH or len(text.split()) < MIN_WORDS:
        return "needs_review"

    # --- 7. ALL CAPS SHOUTING ---
    if sum(1 for c in text if c.isupper()) > len(text) * 0.7:
        return "needs_review"

    # --- 8. Excessive punctuation ---
    if text.count('!') > 8 or text.count('?') > 8:
        return "needs_review"

    # --- 9. URL spam (too many links) ---
    urls = re.findall(r'http[s]?://', text_lower)
    if len(urls) > 3:
        return "needs_review"

    # === ALL CHECKS PASSED ===
    return "safe"

def classify_comment(comment_text: str) -> str:
    """
    Run manual checks first, then OpenAI moderation if needed.
    Returns 'needs_review' or 'safe'.
    """
    print("\n=== Manual checks ===")
    manual_result = manual_checks(comment_text)
    
    if manual_result == "blocked":
        print("→ FINAL: BLOCKED (DB risk)")
        return "blocked"

    if manual_result == "flagged":
        print("→ FINAL: FLAGGED (manual heuristics)")
        return "flagged"

    try:
        print("\n--- OpenAI Moderation Request ---")
        print(f"Input text: {comment_text}\n")
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=comment_text
        )

        print("--- OpenAI Moderation Response ---")
        print(response)
        print("-----------------------------\n")

        result = response.results[0]
        flagged = result.flagged

        if flagged:
            print("→ Result: needs_review (flagged)\n")
            return "needs_review"
        else:
            print("→ Result: ok (not flagged)\n")
            return "safe"

    except Exception as e:
        print("Moderation API error:", e)
        return "needs_review"  # Safe fallback
