import requests
import time
import pandas as pd

def get_mozilla_observatory_data(url):
    scan_url = f"https://http-observatory.security.mozilla.org/api/v1/analyze?host={url}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # Initiate a scan
        response = requests.post(scan_url, headers=headers)
        if response.status_code != 200:
            return {"error": f"Failed to initiate scan: {response.status_code}"}
        
        # Get the scan results
        results_url = f"https://http-observatory.security.mozilla.org/api/v1/analyze?host={url}&rescan=true"
        for _ in range(10):  # Retry 10 times
            results_response = requests.get(results_url, headers=headers)
            if results_response.status_code == 200:
                results = results_response.json()
                if results['state'] == 'FINISHED':
                    return results
            time.sleep(10)  # Wait before retrying
        
        return {"error": "Scan did not complete in a timely manner"}
    
    except requests.RequestException as e:
        return {"error": f"Error fetching security metrics: {type(e).__name__} - {e}"}
    



df =  pd.read_csv('wtb_internship_task')

df['security_metrics']=df['Domain name'].apply(get_mozilla_observatory_data)

# Example usage

