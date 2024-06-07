## My approach

The first goal was to  analyze  the reasons and the benefits that an e-commerce website can have from migrating their website to Shopify.  I started with  doing a research why a e-commerce website would want to  migrate their website to shopify and I came up with these reasons.

* Better SEO ranking, easier SEO optimization
* Better scalability
* Better security
* More payment options
* Mobile friendliness

After   this step, I began to do a research about how can i automize the  process of  measuring these indicators about a website. Here is the summary of the apis that helped me to  analyze these  metrics

* Lighthouse api - an open-source, automated tool for improving the quality of web pages. You can run it against any web page, public or requiring authentication. It has audits for performance, accessibility, progressive web apps, SEO, and more.
* Mozilla Observatory api - The Mozilla Observatory provides web applications assessments which help teach developers, system administrators, and security professionals how to configure their sites safely and securely.
* Locust api - Locust is an open source performance/load testing tool for HTTP and other protocols. Its developer-friendly approach lets you define your tests in regular Python code.


By analyzing these  indicators a website, my aim was to  automize  making an  tailored offer with Large Language models, focusing on the shortcomings of the website in  based

For the comprehensive analysis of  the  e-commerce websites google's lighthouse api is used. Briefly explaining, lighthouse api is an  open source api developed by google to  analyze the performance of the website, such as performance score, seo score, accessibility. You can find more info about the api from this link: [https://developer.chrome.com/docs/lighthouse/overview/](https://developer.chrome.com/docs/lighthouse/overview/).

I used lighthouse api on every website in the list and stored their lighthouse data both for mobile and  desktop factors.

### The structure of final.csv

| Domain name | Company name | Twitter | Facebook | lighthouse_metrics                 | contact_details                 | twitter_details                                                              | security_score |
| ----------- | ------------ | ------- | -------- | ---------------------------------- | ------------------------------- | ---------------------------------------------------------------------------- | -------------- |
| example.com | Example      | example | example  | { 'mobile' :{ }, 'desktop' :{ } } | { 'email' :{} , 'phone': { } } | {'tweets': 763, 'following': 452, 'followers': 686, 'likes': 66, 'media': 0} | 25             |
