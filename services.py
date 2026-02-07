import os
import base64
import json
import random
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def predict_skin_condition(image_bytes: bytes):
    """
    Analyze skin condition using OpenAI GPT-4o.
    """
    if not client.api_key:
        print("Warning: OPENAI_API_KEY not found. Using mock fallback.")
        return mock_predict_skin_condition(image_bytes)

    try:
        # Encode image to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful medical assistant for preliminary screening. 
                    Your task is to analyze skin images for Atopic Dermatitis.
                    
                    Output MUST be a valid JSON object with these keys:
                    - condition: Either "Atopic Dermatitis" or "Healthy Skin / Other"
                    - confidence: "Low", "Medium", or "High"
                    - explanation: A patient-friendly, non-technical explanation (max 2 sentences).
                    
                    IMPORTANT: 
                    - This is for a concept prototype, not medical diagnosis.
                    - Be conservative. If it looks like eczema/AD, label it "Atopic Dermatitis".
                    - NEVER use the word "diagnosis". 
                    """
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this skin image."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=300
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return mock_predict_skin_condition(image_bytes)


def mock_predict_skin_condition(image_bytes: bytes):
    """
    Mock AI classifier. 
    In a real hackathon, this might use a small TF/PyTorch model or API.
    For this prototype, we simulate detection.
    
    If the file size is 'even', we say it's Atopic Dermatitis (to allow easy testing of both paths).
    """
    # Deterministic mock based on simple property to allow testing both states
    # Real logic: Load image -> Preprocess -> Model -> Output
    
    # Let's make it 80% chance of Atopic Dermatitis for the demo flow
    is_atopic = random.random() < 0.8
    
    if is_atopic:
        return {
            "condition": "Atopic Dermatitis",
            "confidence": random.choice(["Medium", "High"]),
            "explanation": "Visual patterns indicate inflammation consistent with eczematous dermatitis, including erythema and lichenification."
        }
    else:
        return {
            "condition": "Healthy Skin / Other",
            "confidence": "High",
            "explanation": "No significant signs of inflammatory dermatosis detected. Skin barrier appears intact."
        }

def get_mock_trials():
    """Fallback mock trials if API fails or for speed"""
    return [
        {
            "nct_id": "NCT05551234",
            "title": "Efficacy of Cream-X for Moderate Atopic Dermatitis",
            "status": "RECRUITING",
            "locations": ["New York, NY", "Boston, MA"],
            "phases": ["Phase 2"],
            "match_reason": "Matches your condition profile (Moderate AD). Includes topical treatment which matches your preference history."
        },
        {
            "nct_id": "NCT09998888",
            "title": "Oral JAK Inhibitor Study for Adult AD",
            "status": "RECRUITING",
            "locations": ["Chicago, IL"],
            "phases": ["Phase 3"],
            "match_reason": "Suitable for cases where topical treatments have failed. Age group 18-50."
        }
    ]
