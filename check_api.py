import requests
import json

def check_api():
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.cond": "Atopic Dermatitis",
        "filter.overallStatus": "RECRUITING",
        "pageSize": 1,
        "fields": "NCTId,BriefTitle,OverallStatus,Phase,EligibilityCriteria,LocationCity,LocationState"
    }
    
    # Note: field names in 'fields' param must match the dot notation or specific keys allowed by v2. 
    # The user provided metadata suggests the structure is deeply nested.
    # Let's try to request the fields using the module notation if the simple aliases don't work, 
    # or just fetch everything (minimal fields) to check structure.
    
    # Let's try a broader query first without strict fields to see the natural structure
    params_broad = {
        "query.cond": "Atopic Dermatitis",
        "filter.overallStatus": "RECRUITING",
        "pageSize": 1
    }

    try:
        print("Fetching from ClinicalTrials.gov API...")
        response = requests.get(url, params=params_broad, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "studies" in data and len(data["studies"]) > 0:
            print("Successfully fetched a study.")
            study = data["studies"][0]
            print(json.dumps(study, indent=2))
        else:
            print("No studies found or unexpected format.")
            print(json.dumps(data, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_api()
