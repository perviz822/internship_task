import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from multiprocessing import Pool
from tqdm import tqdm
import random
import time
from fake_useragent import UserAgent

def random_sleep():
    time.sleep(random.uniform(1, 5))

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def extract_contact_info(url):
    original_url = url
    url = f"https://www.{url}"
    email_set = set()
    phone_set = set()  # Using a set to avoid duplicates

    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    # Implement retries
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            break
        except requests.RequestException as e:
            print(f"Request error for {original_url}, attempt {attempt + 1}: {e}")
            random_sleep()
    else:
        return (original_url, {'emails': email_set, 'phones': phone_set})

    try:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract contact info from HTML elements
        for element in soup.find_all(['p', 'div', 'span']):
            text = element.get_text().strip()
            # Example pattern for email address extraction
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, text)
            for email in emails:
                if ' ' not in email:  # Check if email contains no space
                    email_set.add(email)

            phone_pattern = r'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\0-9]*(?=[^0-9])'
            phone_numbers = re.findall(phone_pattern, text)

            # Clean and filter phone numbers
            for number in phone_numbers:
                cleaned_number = re.sub(r'\s+|\n', '', number)  # Remove spaces and newlines
                if len(cleaned_number) >= 10 and (len(cleaned_number<20)):  # Assuming a minimum length of 10 for valid numbers
                    phone_set.add(cleaned_number)
    except Exception as e:
        print(f"Parsing error for {original_url}: {e}")

    # Add random sleep after processing each URL
    random_sleep()
    
    return (original_url, {'emails': email_set, 'phones': phone_set})

print(extract_contact_info('boutiquephotographique.com'))


