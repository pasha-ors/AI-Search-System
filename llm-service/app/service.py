import requests
import os
import json
from dotenv import load_dotenv

import re

def extract_price(text: str):
    text = text.lower()

    min_price = None
    max_price = None

    # від / from / over
    match = re.search(r"(від|from|over)\s*(\d+)", text)
    if match:
        min_price = int(match.group(2))

    # до / under / below
    match = re.search(r"(до|under|below)\s*(\d+)", text)
    if match:
        max_price = int(match.group(2))

    return min_price, max_price

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
    "max_price": null,
    "min_price": null
    }}

    ALLOWED VALUES:
    color: ["black","white","red","blue","green"]
    brand: ["nike","adidas","puma"]
    purpose: ["running","training","casual"]

    RULES:
- Use ONLY allowed values
- ONE value per field (as array)

- Extract brand ONLY if explicitly mentioned
- Extract color ONLY if explicitly mentioned
- Extract purpose ONLY if explicitly mentioned

- Do NOT infer or guess brand, color, or purpose
- If a field is not clearly mentioned → return null

- If input has no clear meaning → return all fields as null

- Output JSON ONLY

    If input has no meaning:
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

    min_price, max_price = extract_price(text)

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
                    data[key] = [str(data[key]).lower()]
                if len(data[key]) > 1:
                    data[key] = [str(data[key][0]).lower()]
                if data[key] == []:
                    data[key] = None

        # 🔥 ОЦЕ ТИ ЗАБУВ
        data["min_price"] = min_price
        data["max_price"] = max_price

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