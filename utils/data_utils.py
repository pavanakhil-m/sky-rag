import json
import re


def extract_json_str(text):
    try:
        # Find the first {...} block (basic JSON object)
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("Invalid JSON found:", e)

    return None


# need to get mmore context - > title, body, author, date, bio if avaliable, thumbnail.
def extract_context_json(data_obj):
    try:
        return data_obj.get("body", "")
    except Exception:
        return ""
