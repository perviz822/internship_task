import pandas as pd
from openai import OpenAI
import json
from multiprocessing import Pool
from tqdm import tqdm
import time
from api_key import return_api_key

def tailored_offer(args):
    domain_name, company_name, lighthouse_metrics, response_time, security_score,contact_details = args
    try:
        client = OpenAI(api_key={return_api_key()})
        message = f"""
        I want you to act as an agent  who works for a company that identifies e-commerce websites that
        can benefit from migrating to Shopify. Your job is to make a tailored 
        offer based on the data you provide. Here's the data from tests like Lighthouse,
        Mozilla Observatory,:

        - Website URL: {domain_name}
        - Company Name: {company_name}
        - Lighthouse Data: {lighthouse_metrics}
        - Mozilla Observatory: {security_score}
        - Get response time: {response_time}

        Act as an agent for a company that
        identifies e-commerce websites that can benefit
        from migrating to Shopify. 
        Make a tailored offer to {company_name}, 
        (if company  name is unknown, then  adress the customer with it's domain name)
        based on provided data. Emphasize the site's shortcomings
        without mentioning any tests or technical details. Highlight
        how migrating to Shopify will benefit the website based on  the shortcomings. Keep the 
        response under 250 words.
        """

        # Retry until a non-empty and complete response is received
        while True:
            response = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[{"role": "user", "content": message}],
                stream=False
            )
            tailored_response = response.choices[0].message.content.strip()
            if tailored_response:
                break
                
        # Replace newline characters with actual new lines
        tailored_response = tailored_response.replace('\n', ' ')
        if company_name!="unknown" :
         return {"company_name": company_name, "tailored_offer": tailored_response, "contact_details":contact_details}
        else:
            return {"domain_name": domain_name, "tailored_offer": tailored_response,"contact_details":contact_details}

    except Exception :
        time.sleep(1)
        return  tailored_offer(args)

def generate_tailored_offer(row):
    return tailored_offer((row['Domain name'], row['Company name'], row['lighthouse_metrics'], row['response_time'], row['security_score'],row['contact_details']))

def main():
    # Assuming 'df' is your DataFrame
    df = pd.read_csv('final11.csv')

    # Use multiprocessing to parallelize the generation of tailored offers
    with Pool() as pool:
        tailored_offers = list(tqdm(pool.imap(generate_tailored_offer, [row for index, row in df.iterrows()]), total=len(df)))

    # Write the list of tailored offers to a JSON file
    with open('tailored_offers_final.json', 'w', encoding='utf-8') as json_file:
        json.dump(tailored_offers, json_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
