import re

def clean_ai_sql(raw_sql):
    """
    Portfolio Highlight: Professional-grade SQL cleaning.
    Removes markdown blocks and common LLM prefix 'sqlite' or 'sql'.
    """
    # 1. Remove Markdown code blocks if they exist
    clean = re.sub(r"```(sql|sqlite)?", "", raw_sql, flags=re.IGNORECASE)
    clean = clean.replace("```", "").strip()
    
    # 2. Find the start of the actual SQL command (SELECT, WITH, etc.)
    # This specifically fixes your 'ite' or 'sqlite' error
    match = re.search(r"(SELECT|WITH|INSERT|UPDATE|CREATE|DROP|PRAGMA|DELETE)\b", clean, re.IGNORECASE)
    if match:
        return clean[match.start():].strip()
    
    return clean