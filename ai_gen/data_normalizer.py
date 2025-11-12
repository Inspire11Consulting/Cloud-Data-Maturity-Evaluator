"""
Baseball card data normalization utilities.
"""

import json


def get_field(case_insensitive_dict, *candidates):
    """
    Helper: given a dict, return first existing field among candidates (case-insensitive).
    
    Args:
        case_insensitive_dict: Dictionary to search
        *candidates: Field names to search for (case-insensitive)
    
    Returns:
        Value of first matching field, or None if not found
    """
    if not isinstance(case_insensitive_dict, dict):
        return None
    for cand in candidates:
        for k in case_insensitive_dict.keys():
            if k.lower() == cand.lower():
                return case_insensitive_dict[k]
    return None


def normalize_baseball_card(parsed):
    """
    Ensure returned object has 'executive' and 'technical' keys.
    Accept a few common variants. Returns normalized dict:
    { "executive": {...}, "technical": {...} }
    
    Args:
        parsed: Parsed JSON object (dict, list, or other)
    
    Returns:
        dict: Normalized structure with 'executive' and 'technical' keys
    """
    if parsed is None:
        return {"executive": {}, "technical": {}}
    if isinstance(parsed, str):
        # cannot parse — return empty and keep raw elsewhere
        return {"executive": {}, "technical": {}}
    if isinstance(parsed, list):
        # unexpected — place in executive.summary
        return {"executive": {"summary": " ".join(map(str, parsed))}, "technical": {}}
    if isinstance(parsed, dict):
        keys_lower = {k.lower(): k for k in parsed.keys()}
        # If already has exec/technical
        if "executive" in parsed and "technical" in parsed:
            return {
                "executive": parsed.get("executive") or {},
                "technical": parsed.get("technical") or {}
            }
        # Accept capitalized variants
        if "Executive" in parsed or "Technical" in parsed:
            return {
                "executive": parsed.get("Executive") or parsed.get("executive") or {},
                "technical": parsed.get("Technical") or parsed.get("technical") or {}
            }
        # Some outputs may return top-level fields for executive only
        # Heuristic: if keys include summary/recommendation/activities -> treat as executive
        exec_keys = {"summary", "recommendation", "activities", "project_activities", "focus_8w", "plan_3y", "assumptions", "team"}
        lower_keys = {k.lower() for k in parsed.keys()}
        if lower_keys & exec_keys:
            # map fields to canonical names if necessary
            exec_block = {}
            tech_block = {}
            for k, v in parsed.items():
                kl = k.lower()
                if kl in exec_keys:
                    # unify 'project_activities' -> 'activities'
                    if kl == "project_activities":
                        exec_block.setdefault("activities", v)
                    else:
                        exec_block[kl] = v
                else:
                    # put other keys under exec by default
                    exec_block[k] = v
            return {"executive": exec_block, "technical": tech_block}
        # If parsed contains exactly two top-level keys that look like cards (e.g., 'Exec' and 'Tech'), map them
        if len(parsed.keys()) <= 4:
            # attempt mapping by inspection
            exec_block = parsed.get("executive") or parsed.get("Executive") or {}
            tech_block = parsed.get("technical") or parsed.get("Technical") or {}
            return {"executive": exec_block, "technical": tech_block}
        # fallback: put entire parsed content into executive.summary as string
        return {"executive": {"summary": json.dumps(parsed)[:1000]}, "technical": {}}
    # else fallback
    return {"executive": {}, "technical": {}}

