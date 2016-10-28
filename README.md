# housing_alerts

This is a light-weight package to search craigslist apartment listings and email any relevant ones to your email account. I run it on EC2 with CRON scheduling.

The search URL and other parameters are specified in `configs.py`. Email addresses and authentication info should be defined in environment variables. If you don't want
to use your personal email account to send messages, I would recommend signing up
for a hotmail account and use `FROM_EMAIL_PORT=587` and `FROM_EMAIL_SMTPSERVER=smtp.live.com`.

Every time the `search_listings` script is run, it searches craigslist, downloads the listings, and if there are any new ones compared to the last search, it sends an email to the account specified in the configuration.
