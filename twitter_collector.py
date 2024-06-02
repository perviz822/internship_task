import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

MAX_RETRIES = 3



def get_twitter_user_description(username):
    # Set up ChromeOptions
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    
    driver = None
    for _ in range(MAX_RETRIES):
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            break
        except Exception as e:
            print(f"Failed to initialize Chromedriver. Retrying... Error: {e}")

    if driver is None:
        print("Failed to initialize Chromedriver after multiple retries. Aborting.")
        return None

    try:
        # Navigate to the user's Twitter page
        driver.get(f"https://twitter.com/{username}")

        # Wait for the user description element to be present in the DOM
        user_description_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="UserDescription"]'))
        )

        # Extract the text from the span element inside the user description div
        user_description = user_description_element.find_element(By.TAG_NAME, 'span').text

        # Wait for the followers count element to be present in the DOM
        followers_count_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3.r-1b43r93.r-1cwl3u0.r-b88u0q'))
        )

        # Extract the text from the followers count span element
        followers_count = followers_count_element.text

        # Wait for the tweet count element to be present in the DOM
        tweet_count_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), " posts")]'))
        )

        # Extract the text from the tweet count div element
        tweet_count = tweet_count_element.text

        # Locate the parent element containing the "Joined" date
        joined_date_parent_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="UserProfileHeader_Items"]'))
        )
        try:
            joined_date_element = joined_date_parent_element.find_element(By.CSS_SELECTOR, 'span[data-testid="UserJoinDate"]')
            joined_date = joined_date_element.text
        except Exception as e:
            print(f"Failed to locate 'Joined' date element: {e}")
            try:
                joined_date_element = joined_date_parent_element.find_element(By.CSS_SELECTOR, 'span[data-testid="UserJoinDate"]')
                joined_date = joined_date_element.text
            except Exception as e:
                print("retry to locate failed again")
             

            joined_date = "N/A"

        return [user_description, followers_count, tweet_count, joined_date]
    except Exception as e:
        print(f"An error occurred: {e}")
        # Retry the operation one more time
        try:
            driver.refresh()
            return get_twitter_user_description(username)
        except Exception as e:
            print(f"Failed to retry operation: {e}")
            return None
    finally:
        if driver:
            driver.quit()


users = ['ch_saintmartin', 'brusselskitchen', 'sens_uniques','massanois','cantinebio']
data_list = []

start = time.perf_counter()
for user in users:
    data = get_twitter_user_description(user)
    if data:
        data_list.append(data)
    
end = time.perf_counter()

print(f"Scraping took {end - start} seconds.")
print(data_list)
