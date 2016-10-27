# housing_alerts

This is a light-weight package to search craigslist apartment listings and email any relevant ones to your email account. I run it on EC2 with CRON scheduling. 

The search URL and other parameters are specified in `configs.py`, and email authentication info should be stored in `special_configs.py`, which is not included here and should be created manually.

Every time the main script is run, it searches craigslist, downloads the listings, and if there are any new ones compared to the last search, it sends an email to the account specified in `special_configs.py`.
