import subprocess
import json
from multiprocessing import Pool
import pandas as pd



def get_lighthouse_data(url, timeout=300):  # 5-minute timeout
    url = "https://www.{url}".format(url)
    reports = {'mobile': {}, 'desktop': {}}
    
    for factor in ['mobile', 'desktop']:
        try:
            command = (
                f"lighthouse {url} "
                f"--output=json "
                f"--chrome-flags='--headless' "
                f"--emulated-form-factor={factor}"
            )
            
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(timeout=timeout)

            if process.returncode != 0:
             error_message = stderr.decode('utf-8').splitlines()[0]
             if "No usable browser" in error_message:
                 return (url, "Error: Chrome browser not found")
             else:
                 return (url, f"Lighthouse audit failed: {error_message}")

            report = json.loads(stdout.decode('utf-8'))
            reports[factor] = report

        except (json.JSONDecodeError, KeyError) as e:
            return (url, f"Error parsing results: {type(e).__name__} - {e}")
        except Exception as e:
            return (url, f"Unexpected error: {type(e).__name__} - {e}")
    
    return (url, reports)

def main():
    df = pd.read_csv('wtb-internship-test.csv')
    domain_names = df['Domain name'].tolist()
    with Pool() as pool:
        results = pool.map(get_lighthouse_data, domain_names)

    lighthouse_df = pd.DataFrame(results, columns=['url', 'lighthouse_score'])
    lighthouse_df.to_csv('lighthouse.csv', index=False)

if __name__ == '__main__':
    main()
