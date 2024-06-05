import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
def extract_contact_info(url):
    # Method 1: Parsing HTML
    url = "https://www.{url}".format(url=url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    contact_info = set()  # Using a set to avoid duplicates

    # Extract contact info from HTML elements
    for element in soup.find_all(['p', 'div', 'span']):
        text = element.get_text().strip() 
        # Example pattern for email address extraction
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        for email in emails:
            if ' ' not in email:  # Check if email contains no space
                contact_info.add(email)
        
        phone_pattern = r'[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\0-9]*(?=[^0-9])'
        french_phone_numbers = re.findall(phone_pattern, text)
        
        # Clean and filter phone numbers
        for number in french_phone_numbers:
            cleaned_number = re.sub(r'\s+|\n', '', number)  # Remove spaces and newlines
            if len(cleaned_number) >= 10:  # Assuming a minimum length of 10 for valid numbers
                contact_info.add(cleaned_number)


    return contact_info



url= '3rdragon.ca'
contact_info = extract_contact_info(url)
print(contact_info)

#df =  pd.read_csv('wtb_internship_task')

#df['security_metrics']=df['Domain name'].apply(extract_contact_info)


   
