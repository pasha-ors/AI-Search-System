import requests
import os
import json
from dotenv import load_dotenv

# --- ENV ---
load_dotenv()
OLLAMA_URL = os.getenv("OLLAMA_URL") or "http://localhost:11434"
MODEL = os.getenv("MODEL") or "llama3"

# --- DEFAULT RESULT ---
def empty_result():
    return {
        "color": None,
        "brand": None,
        "purpose": None,
        "max_price": None,
        "min_price": None
    }

# --- JSON EXTRACTOR ---
def extract_json(raw: str):
    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1:
        return None

    try:
        return json.loads(raw[start:end + 1])
    except:
        return None

# --- MAIN ---
def analyze_text(text: str):

    prompt = f"""
    Extract structured data from sneaker query.

    Return ONLY valid JSON.

    SCHEMA:
    {{
    "color": string[] | null,
    "brand": string[] | null,
    "purpose": string[] | null,
    "max_price": number | null,
    "min_price": number | null
    }}

    ALLOWED VALUES:
    color: ["black","white","red","blue","green"]
    brand: ["nike","adidas","puma"]
    purpose: ["running","training","casual"]

    RULES:
    - Use ONLY allowed values
    - ONE value per field (as array)
    - Do NOT guess brand or color
    - Extract ONLY if explicitly mentioned
    - If not clearly mentioned → null
    - Purpose can be inferred from meaning
    - "under X" / "до X" → max_price
    - "over X" / "від X" → min_price
    - Extract value ONLY if it is explicitly mentioned in the text
    - Do NOT infer or assume color or brand
    - If the user did not clearly mention it → return null

    If input has no meaning, return:
    {{
    "color": null,
    "brand": null,
    "purpose": null,
    "max_price": null,
    "min_price": null
    }}

    OUTPUT:
    JSON ONLY. NO TEXT.

    INPUT:
    "{text}"
    """

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0}
            },
            timeout=60
        )

        if r.status_code != 200:
            return empty_result()

        raw = r.json().get("response", "")

        data = extract_json(raw)

        if not data:
            return empty_result()

        # --- NORMALIZE ---
        for key in ["color", "brand", "purpose"]:
            if key in data:
                if data[key] is None:
                    continue
                if not isinstance(data[key], list):
                    data[key] = [data[key]]
                if len(data[key]) > 1:
                    data[key] = [data[key][0]]

        # --- PRICE SAFE ---
        for key in ["max_price", "min_price"]:
            if key in data and data[key] is not None:
                try:
                    data[key] = int(data[key])
                except:
                    data[key] = None

        return data

    except:
        return empty_result()