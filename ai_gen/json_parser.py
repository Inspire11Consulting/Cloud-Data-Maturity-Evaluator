"""
Robust JSON parsing utilities with multiple fallback strategies.
"""

import json
import re


def _extract_balanced_json_object(text):
    """Extract the first balanced top-level JSON object from text."""
    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False
    for idx in range(start, len(text)):
        ch = text[idx]

        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : idx + 1]
    return None


def try_load_json(text):
    """
    Robust JSON loader with several fallbacks.
    Returns a Python object (usually dict) or raises ValueError.
    
    Args:
        text: Text that may contain JSON
    
    Returns:
        dict or list: Parsed JSON object
    
    Raises:
        ValueError: If JSON cannot be parsed
    """
    if text is None:
        raise ValueError("No text provided")
    t = str(text).strip().lstrip("\ufeff")

    # If code fence present, extract inner content
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", t, re.IGNORECASE)
    if fence:
        t = fence.group(1).strip()

    # Direct try
    try:
        return json.loads(t)
    except Exception:
        pass

    # Try replace single quotes with double quotes (common model output)
    try:
        return json.loads(t.replace("'", '"'))
    except Exception:
        pass

    # Remove trailing commas before } or ]
    try:
        cleaned = re.sub(r",\s*([}\]])", r"\1", t)
        return json.loads(cleaned)
    except Exception:
        pass

    # Extract first {...} substring
    start = t.find("{")
    end = t.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = t[start:end+1]
        try:
            return json.loads(candidate)
        except Exception:
            # last-ditch: replace single quotes in candidate
            try:
                return json.loads(candidate.replace("'", '"'))
            except Exception:
                pass

    # Extract first balanced JSON object (safer than greedy rfind)
    candidate = _extract_balanced_json_object(t)
    if candidate:
        try:
            return json.loads(candidate)
        except Exception:
            try:
                return json.loads(candidate.replace("'", '"'))
            except Exception:
                pass

    raise ValueError("Could not parse JSON from the model output.")

