import requests
import json

def search_trials():
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.cond": "Atopic Dermatitis",
        "filter.overallStatus": "RECRUITING",
        "pageSize": 5,
        "fields": "NCTId,ProtocolSection.IdentificationModule.BriefTitle,ProtocolSection.StatusModule.OverallStatus,ProtocolSection.DesignModule.PhaseList,ProtocolSection.EligibilityModule.EligibilityCriteria,ProtocolSection.ContactsLocationsModule.LocationList"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_trials()
