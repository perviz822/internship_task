## Data cleaning steps

* Filling missing values  with string "unkown"
* Validation check  domain names
* Validation check for  twitter account names
* Validation check  for facebook account names
* Removing duplicates

## Data preprocessing

Before analyzing the domains, I wanted to ensure that non-functional websites would not be included in the analysis process. Some websites block incoming requests because they do not allow automated request attempts. To mitigate this, I included user agent headers to humanize the requests and avoid such blocks. The websites eliminated in this process responded with the following status codes:

* **404 Not Found** : This status code means that the server cannot find the requested resource. It indicates that the website or specific page is no longer available at the requested URL.
* **410 Gone** : This status code is more specific than 404. It means that the resource requested is no longer available and will not be available again. This is often used when a website has been permanently taken down.
* **500 Internal Server Error** : This is a generic error message given when the server encounters an unexpected condition that prevents it from fulfilling the request. It often indicates a problem with the website's server.
* **503 Service Unavailable** : This status code indicates that the server is currently unable to handle the request due to temporary overloading or maintenance of the server. It suggests that the website is temporarily down.
* **522 Connection Timed Out** (specific to Cloudflare): This indicates that the server is taking too long to respond, often due to network issues or server overload.

## Contact details scraping

The script is designed to scrape contact information (emails and phone numbers) from a given website URL.

#### Key Components

1. **Libraries Used:**

   - `requests`: For making HTTP requests.
   - `BeautifulSoup` from `bs4`: For parsing HTML content.
   - `re`: For regular expression operations.
   - `Pool` from `multiprocessing`: For parallel processing.
   - `tqdm`: For displaying progress bars.
   - `random` and `time`: For random sleep intervals.
   - `UserAgent` from `fake_useragent`: For generating random user agents to avoid being flagged as a bot
2. **Functions:**

   - `random_sleep()`: Pauses execution for a random time between 1 to 5 seconds to avoid being flagged as a bot.
   - `get_random_user_agent()`: Returns a random user agent string to mimic different browsers and reduce the chance of being blocked.
3. **Main Function:**

   - `extract_contact_info(url)`: Scrapes the specified URL to extract email addresses and phone numbers.

#### Function Workflow

1. ##### **Initialization:**


   - The URL is formatted to ensure it starts with `https://www.`
   - Empty sets for emails and phone numbers are initialized to store unique contact information.
2. **HTTP Request with Retry:**

   - HTTP request headers include a random user agent.
   - Up to three attempts are made to fetch the URL content, with a random sleep interval between retries in case of errors.
3. **HTML Parsing and Data Extraction:**

   - The fetched content is parsed using BeautifulSoup.
   - Text is extracted from `<p>`, `<div>`, and `<span>` tags.
   - Regular expressions are used to find and validate email addresses and phone numbers within the extracted text.
   - Valid emails (without spaces) and phone numbers (cleaned and within a reasonable length) are added to the respective sets.
4. **Error Handling:**

   - Any request or parsing errors are caught and printed, allowing the function to continue processing.
5. **Random Sleep:**

   - A random sleep interval is added after processing each URL to avoid detection.
6. **Return Value:**

   - The function returns a tuple containing the original URL and a dictionary with the extracted emails and phone numbers.

## Twitter account scraping

#### Key Components

1. **Libraries Used:**
   - `Nitter` from `ntscraper`: For scraping Twitter profile information.
   - `pandas`: For reading from and writing to CSV files.

#### How It Works

1. **Initialization:**

   - A `Nitter` scraper instance is created with specific settings.
2. **Wrapper Function:**

   - A function  is defined to fetch Twitter profile information, handling any potential errors during the process.
3. **CSV Processing:**

   - The script reads a CSV file containing domain names and Twitter usernames.
   - For each row in the DataFrame, if the Twitter username is known, it fetches the profile information using the wrapper function.
   - The fetched information is stored in a new column in the DataFrame.
4. **Updating CSV File:**

   - The updated DataFrame, now containing Twitter profile information, is written back to the CSV file.

## My approach to the problem

The first goal was to  analyze  the reasons and the benefits that an e-commerce website can have from migrating their website to Shopify.  I started with  doing a research why a e-commerce website would want to  migrate their website to shopify and I came up with these reasons.

* Better SEO ranking, easier SEO optimization
* Better scalability
* Better security
* More payment options
* Mobile friendliness

After   this step, I began to do a research about how can i automize the  process of  measuring these indicators about a website. Here is the summary of the apis that helped me to  analyze these  metrics

* **For automizing  mobile friendliness, seo, accessibility, performance metrics test** :  Lighthouse api - an open-source, automated tool for improving the quality of web pages. You can run it against any web page, public or requiring authentication. It has audits for performance, accessibility, progressive web apps, SEO, and more.
* **For automizing  security test:** Mozilla Observatory api - The Mozilla Observatory provides web applications assessments which help teach developers, system administrators, and security professionals how to configure their sites safely and securely.
* **For automizing scalability test** :  Locust api - Locust is an open source performance/load testing tool for HTTP and other protocols. Its developer-friendly approach lets you define your tests in regular Python code.

By  extracting these information, my goal was to use these information in the prompt   to LLM when making a tailored offer and ask it to focus on the specific  benefits of migrating to shopify if the  the website's  performance in that area is poor.

Lighthouse documentation: [https://developer.chrome.com/docs/lighthouse/overview/](https://developer.chrome.com/docs/lighthouse/overview/).

Mozilla Observatory documentation : [https://github.com/mozilla/http-observatory](https://github.com/mozilla/http-observatory)

Locust documentation : [https://docs.locust.io/en/stable/](https://docs.locust.io/en/stable/)

## The structure of final.csv

| Domain name | Company name | Twitter | Facebook | lighthouse_metrics                 | contact_details                  | twitter_details                                                              | security_score |
| ----------- | ------------ | ------- | -------- | ---------------------------------- | -------------------------------- | ---------------------------------------------------------------------------- | -------------- |
| example.com | Example      | example | example  | { 'mobile' :{ }, 'desktop' :{ } } | { 'email' :{ } , 'phone': { } } | {'tweets': 763, 'following': 452, 'followers': 686, 'likes': 66, 'media': 0} | 25             |

* **lighthouse_metrics** type :  python dict
* **contant_details** type:  python dict
* **twitter_details** type: python dict
* **security_score**  type: string

### Scalability Test

The scalability results for the websites are stored in a separate JSON file. This JSON file contains scalability metrics for various URLs.

#### Structure of the  Locust reposts JSON File

```json
[
    {
        "Domain name": "example.com",
        "Average Response Time": "3400 (in milliseconds)",
        "Requests/s": "27.4",
        "Request Count": "1200",
        "Failure Count": "54",
        "Failure/Response percentage": (54 / 1200) * 100
    },
    {
        "Domain name": "example2.com",
        "Average Response Time": "4555 (in milliseconds)",
        "Requests/s": "23",
        "Request Count": "1110",
        "Failure Count": "33",
        "Failure/Response percentage": (33 / 1110) * 100
    }
]
```

#### Fields Description

- **Domain name**: The domain of the website.
- **Average Response Time**: The average time taken to respond, in milliseconds.
- **Requests/s**: The number of requests processed per second.
- **Request Count**: The total number of requests made during the test.
- **Failure Count**: The number of failed requests.
- **Failure/Response percentage**: The percentage of failed requests out of the total requests, calculated as `(Failure Count / Request Count) * 100`.


## Using Large Language model to make a tailored offer

After gathering data  about  qualified  leads,  I have used  chat gpt 3.5  turbo model to generate a tailored offer  based on the data  provided for each website . I have made api request to  the model, for each website,  and   each request contains  the data I have gathered from apis, from lighthouse, mozilla  observatory, get request  time. This api call is being made for each  domain name in the final.csv file.

```python


def tailored_offer(args):
    domain_name, company_name, lighthouse_metrics, response_time, security_score,contact_details = args
    try:
        client = OpenAI(api_key="my_api_key")
        message = f"""
        I want you to act as an agent  who works for a company that identifies e-commerce websites that
        can benefit from migrating to Shopify. Your job is to make a tailored 
        offer based on the data I provide. Here's the data from tests like Lighthouse,
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
```

for each website  arguments are passed and api call is made. Then the response  is in the form of json object here is the structure of the  json file that stored the responses for the websites.:

```json
[{
    "company_name": "Recettes d'une crétoise",
    "tailored_offer": "Dear Recettes d'une crétoise,  We have recently conducted an analysis of your website and have identified areas where migrating to Shopify could greatly benefit your online presence. Our team noticed that there are certain shortcomings with your current e-commerce platform that could be hindering your website's performance and accessibility for users.  By migrating to Shopify, you will be able to improve your website's overall performance, accessibility, and user experience. Shopify offers a user-friendly interface that can help streamline the checkout process and improve customer satisfaction. Additionally, Shopify's built-in SEO features can help boost your website's visibility and attract more potential customers.  We believe that making the switch to Shopify will not only enhance your website's performance but also help drive more traffic and ultimately increase your sales. Our team is here to support you every step of the way in making this transition smooth and successful.  We look forward to the opportunity to discuss this further with you and help you take your online business to the next level.  Best regards, [Your Name] [Company Name]",
    "contact_details": "{'emails': set(), 'phones': set()}"
  },
  {
    "company_name": "Mam'Ayoka",
    "tailored_offer": "Dear Mam'Ayoka,  I have carefully reviewed your website mamayoka.fr and noticed some areas that could benefit from improvement. By migrating to Shopify, you can enhance the overall performance and accessibility of your site, leading to a better user experience for your customers. Shopify's optimization features can help boost your website's SEO and enhance its overall visibility online.  With a faster response time and improved security measures, Shopify can provide a more reliable platform for your e-commerce operations. Additionally, Shopify's user-friendly interface and customizable design options can help elevate the look and feel of your website, ultimately attracting more customers and driving sales.  I believe that migrating to Shopify can significantly benefit Mam'Ayoka by addressing these shortcomings and maximizing the potential of your online store. If you are interested in learning more about how Shopify can enhance your e-commerce presence, please feel free to reach out for a personalized consultation.  Best regards, [Your Name] Shopify Migration Agent",
    "contact_details": "{'emails': {'acontact@mamayoka.comCommandes', 'contact@mamayoka.com'}, 'phones': set()}"
  }]
```

## Problems and how I have solved them

**Time-Intensive Procedures** While some data gathering processes, such as collecting contact details and Twitter scraping, do not take much time, running a Lighthouse test for a given website is significantly more time-consuming. Each Lighthouse test takes approximately 45 seconds to complete. When scaling this to 2022 websites, the total time required would be about 25 hours. However, by utilizing Python's `multiprocessing` library with a `Pool`, I have successfully reduced the total processing time from 25 hours to 3.5 hours.

**Handling Website Response Rejections Against Bot Requests**  A considerable number of websites returned a 403 HTTP response code, indicating that the websites have measures in place to avoid responding to bot requests. To mitigate this issue, I included a user agent in the request header. For websites that required multiple requests, I used a random user agent generator to provide a different user agent for each call, effectively bypassing some of the anti-bot mechanisms.

**Large Language Model Rate Limit** When using the Chat-GPT-Turbo-3.5 API, I encountered rate limit issues. The API restricts the number of requests you can send within a minute. To address this, I implemented a logic that waits for a second when a rate limit is reached before retrying the call. This approach helps manage the rate limits and ensures continuous operation of the data gathering process.

## **Future Improvements**

**Increasing the Robustness of Phone Number Scraping Methods**  While the existing phone number scraping methods successfully extract phone numbers when available, they sometimes mistakenly extract numbers that are not phone numbers due to the variety of phone number formats and text styles. Enhancing the robustness of these methods is essential to improve accuracy and reliability.

**Language Model Upgrade**  Although the Chat-GPT-3.5-turbo model performs adequately in creating tailored offers based on the provided data of a given website, using the latest models, such as GPT-4, significantly improves the results. The difference is evident in how effectively the upgraded model analyzes the given data, ensuring that no critical points are missed.

**Incorporating Scalability Data in the Tailored Offer** Although the Locust API is used to measure the scalability of a website, its results are not currently emphasized in the tailored offers. A comprehensive Locust API scalability test takes approximately 30 minutes to one hour. I have conducted these tests for only 500 websites, with each test running for one minute. While the results provide a basic comparison of different websites' scalability, they do not offer thorough information. Incorporating detailed scalability data into the tailored offers could enhance the value and precision of the recommendations.

**Facebook scraping**  Even though I have tried different scraping libraries,  none of them worked properly, it's a result of  facebook's strict policy against  scraping. In the future we can work on this problem, and  try differnet various methods, to achieve this.

**Scraping method to gather information about website's  payment options** I have tried scraping  payment methods for a given  websites.  I could not find a common pattern for website structure to gather info about payment methods. This information can be given as an argument to  large language  model, to   focus on the    "many payment options" advantage of the  shopify in the offer.
