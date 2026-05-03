import os
import json
from google import genai


def analyse_meal(description: str) -> dict:
    """
    Takes a natural language meal description like "2 boiled eggs and a glass of milk"
    and returns a dict with estimated nutrition values.

    Returns:
        {
            "food_name": "2 Boiled Eggs and Glass of Milk",
            "calories":  230,
            "protein":   18.0,
            "carbs":     12.0,
            "fats":      11.0,
            "meal_type": "breakfast",
            "quantity":  1
        }

    Raises:
        ValueError      if AI response cannot be parsed
        EnvironmentError if API key is missing
        Exception       for API errors
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise EnvironmentError('GEMINI_API_KEY is not set in .env')

    client = genai.Client(api_key=api_key)

    prompt = f"""You are a nutrition expert. Analyse the following meal description and estimate its nutritional content.
                 Meal: "{description}"
     
                 Respond with ONLY a valid JSON object — no explanation, no markdown, no extra text.
                 Use these exact keys:
                 {{
                   "food_name":  "<concise readable name for the meal>",
                   "calories":   <integer, total kcal>,
                   "protein":    <float, grams>,
                   "carbs":      <float, grams>,
                   "fats":       <float, grams>,
                   "meal_type":  "<one of: breakfast, lunch, dinner, snack>",
                   "quantity":   1
                 }}
     
                 Rules:
                 - Estimate based on typical serving sizes if quantities are not specified.
                 - Round calories to nearest integer.
                 - Round macros to one decimal place.
                 - Infer meal_type from context clues (e.g. "with my morning coffee" → breakfast). Default to "snack" if unclear.
                 - food_name should be short and readable, e.g. "2 Boiled Eggs & Milk" not the full description.
                 - Return ONLY the JSON object. No markdown fences. No explanation."""
                 
    response = client.models.generate_content(
        model    = "gemini-2.5-flash",
        contents = prompt,
    )

    raw = response.text
    if raw is None:
        raise ValueError("Gemini returned empty response")
    raw = raw.strip()

    # Strip markdown fences if model wraps in ```json ... ```
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini returned invalid JSON: {raw}") from e

    # Validate required keys
    required = ["food_name", "calories", "protein", "carbs", "fats", "meal_type", "quantity"]
    missing  = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Response missing keys: {missing}")

    # Sanitise types
    data["calories"] = int(data["calories"])
    data["protein"]  = round(float(data["protein"]), 1)
    data["carbs"]    = round(float(data["carbs"]), 1)
    data["fats"]     = round(float(data["fats"]), 1)
    data["quantity"] = 1

    return data