from ntscraper import Nitter
import pandas as pd

scraper = Nitter(log_level=1, skip_instance_check=False)

df = pd.read_csv("twitter.csv")

def get_profile_info_wrapper(username):
    try:
        return scraper.get_profile_info(username)
    except Exception as e:
        print(f"Error fetching info for {username}: {e}")
        return e  # Or a default value like {} for an empty dictionary

# Apply the wrapper function to the first 10 rows with valid Twitter handles

df = pd.read_csv('twitter_profile_details.csv')


df['twitter_details'] = df['Twitter'].apply(get_profile_info_wrapper)


df.to_csv('twitter_profile_details_updated.csv')

print(df)

