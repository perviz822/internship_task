import subprocess
import json
from multiprocessing import Pool
import time

def get_lighthouse_data(url, timeout=300):  # 5-minute timeout
    url = f"https://www.{url}"
    reports = {'mobile': {}, 'desktop': {}}
    
    for factor in ['mobile', 'desktop']:
        try:
            command = f"lighthouse {url} --output=json --chrome-flags='--headless' --emulated-form-factor={factor}"
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
    urls = ['parenchere.com', 'chocomotive.ca', '16cafe.com', 'marcheauxvins.com','casino-gujanmestras.fr','morelchocolatier.com','rivercafe.fr']
    start_time =  time.perf_counter()
    # Use a process pool
    with Pool() as pool:
        results = pool.map(get_lighthouse_data, urls)

    end_time =  time.perf_counter()

    print("It took only",end_time-start_time,"seconds")



    # Process the results after all processes have completed
    for url, result in results:
        if isinstance(result, str):
            print(f"{url}: {result}")
        else:
            print(f"{url}: Audit completed successfully (see report for details)")
            #print(result) 
    print("It took only",end_time-start_time,"seconds")        

if __name__ == '__main__':
    main()
