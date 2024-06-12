import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Function to make GET request and measure response time
def get_response_time(domain):
    url = f"http://{domain}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return (domain, response.elapsed.total_seconds(), None)
        else:
            return (domain, None, response.status_code)
    except requests.RequestException as e:
        return (domain, None, str(e))

# Function to process the DataFrame
def process_domains(df, column_name='Domain name', output_column='response_time'):
    domains = df[column_name].tolist()
    results = []
    
    # Using ThreadPoolExecutor to make parallel requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_response_time, domain): domain for domain in domains}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing domains"):
            domain, response_time, error = future.result()
            if response_time is not None:
                results.append((domain, response_time))
            else:
                results.append((domain, error))
    
    # Creating a response DataFrame to merge with the original DataFrame
    response_df = pd.DataFrame(results, columns=[column_name, output_column])
    
    # Merging the response times/errors back into the original DataFrame
    df = df.merge(response_df, on=column_name, how='left')
    
    return df

# Example usage
if __name__ == "__main__":
    # Sample data
    df = pd.read_csv('final.csv')
    
    # Process the domains
    df_with_response_times = process_domains(df)
    df_with_response_times.to_csv('status.csv')
    
    # Print the resulting DataFrame
    print(df_with_response_times)
