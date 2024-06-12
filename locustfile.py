import pandas as pd
from openai import OpenAI
import json

def tailored_offer(args):
    domain_name, company_name, lighthouse_metrics, response_time, security_score = args
    print(args)
    client = OpenAI(api_key="sk-proj-mSBfqI8NYhHk9Qe2Fp94T3BlbkFJ5dlYScUzmKVjjU7UOxUf")
    message = f"""
    I want you to act as an agent  who works for a company that identifies e-commerce websites that
    can benefit from migrating to Shopify. Your job is to make a tailored 
    offer based on the data you provide. Here's the data from tests like Lighthouse,
    Mozilla Observatory, {company_name}:

    - Website URL: {domain_name}
    - Company Name: {company_name}
    - Lighthouse Data: {lighthouse_metrics}
    - Mozilla Observatory: {security_score}
    - Get response time: {response_time}

    Act as an agent for a company that
    identifies e-commerce websites that can benefit
    from migrating to Shopify. 
    Make a tailored offer to {company_name}
    based on provided data. Emphasize the site's shortcomings
    without mentioning any tests or technical details. Highlight
    how migrating to Shopify will benefit the website. Keep the 
    response under 200 words.
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
            
    return {"company_name": company_name, "tailored_offer": tailored_response}
       

def main():
    # Assuming 'df' is your DataFrame
    df = pd.read_csv('final10.csv').head(5)

    # Create an empty list to store tailored offers
    tailored_offers = []

    # Apply the function to each row in the DataFrame
    for index, row in df.iterrows():
        tailored_offers.append(tailored_offer((row['Domain name'], row['Company name'], row['lighthouse_metrics'], row['response_time'], row['security_score'])))

    # Write the list of tailored offers to a JSON file
    with open('your_output.json', 'w') as json_file:
        for offer in tailored_offers:
            json.dump(offer, json_file)
            json_file.write('\n')

if __name__ == "__main__":
    main()
