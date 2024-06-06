import requests
import time
import pandas as pd
from multiprocessing import Pool
from tqdm import tqdm

def get_mozilla_observatory_data(url):
    scan_url = f"https://http-observatory.security.mozilla.org/api/v1/analyze?host={url}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # Initiate a scan
        response = requests.post(scan_url, headers=headers)
        if response.status_code != 200:
            return (url, f"Failed to initiate scan: {response.status_code}")
        
        # Get the scan results
        results_url = f"https://http-observatory.security.mozilla.org/api/v1/analyze?host={url}&rescan=true"
        for _ in range(10):  # Retry 10 times
            results_response = requests.get(results_url, headers=headers)
            if results_response.status_code == 200:
                results = results_response.json()
                if results['state'] == 'FINISHED':
                    return (url, results.get('score'))
            elif results_response.status_code != 200:
                return (url, f"Failed to get scan results: {results_response.status_code}")
            time.sleep(10)  # Wait before retrying
        
        return (url, "Scan did not complete in a timely manner")
    
   
    except Exception as e:
          return (url, f"Error fetching security metrics: {type(e).__name__} - {e}")


def main():
    df = pd.read_csv('final3.csv')
    domain_names = df['Domain name'].tolist()
    print(len(domain_names))
   
    with Pool() as pool:
        results = []
        for result in tqdm(pool.imap_unordered(get_mozilla_observatory_data, domain_names), total=len(domain_names)):
            results.append(result)
    
    # Convert the results to a DataFrame and save to CSV
    lighthouse_df = pd.DataFrame(results, columns=['url', 'score'])
    lighthouse_df.to_csv('security.csv', index=False)

if __name__ == '__main__':
    main()
