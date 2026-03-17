"""
Robust JSON parsing utilities with multiple fallback strategies.
"""

import json
import re


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
    t = str(text).strip()

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

    raise ValueError("Could not parse JSON from the model output.")

