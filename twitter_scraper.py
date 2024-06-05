from ntscraper import Nitter
import pandas as pd

scraper = Nitter(log_level=1, skip_instance_check=False)

df = pd.read_csv("twitter.csv")

def get_profile_info_wrapper(username):
    try:
        return scraper.get_profile_info(username)
    except Exception as e:
        print(f"Error fetching info for {username}: {e}")
        return e  





df = pd.read_csv('wtb-internship-test.csv')
df['twitter_details'] = df.apply(lambda row: get_profile_info_wrapper(row['Domain_name']) 
                                     if row['Twitter'].lower() != 'unknown' else None, axis=1)
df.to_csv('wtb-internship-test.csv')
