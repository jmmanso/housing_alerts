import os
thisdir = os.path.dirname(__file__)

# Specify Craigslist search url
cl_search_url = "https://sfbay.craigslist.org/search/sfc/apa?hasPic=1&nh=4&nh=12&nh=18&max_price=2700&bedrooms=1&bathrooms=1&availabilityMode=0"

# Specify other urls
dolores_search_url240 = "http://www.240doloresapts.com/floorplan/1x1/"
dolores_search_url230 = "http://www.230doloresapts.com/floorplan/1x1/"

# Path to save results
cl_dump_json_path = thisdir+"/files/cl_historic.json"
cl_new_json_path = thisdir+"/files/cl_new.json"

# Email information is retrieved from environment variables,
# which you need to set beforehand
try:
    from_email_address = os.environ['FROM_EMAIL_ADDRESS']
    from_email_smtpserver = os.environ['FROM_EMAIL_SMTPSERVER']
    from_email_port = int(os.environ['FROM_EMAIL_PORT'])
    from_email_pswd = os.environ['FROM_EMAIL_PSWD']
    to_email_address = os.environ['TO_EMAIL_ADDRESS']
except KeyError:
    raise Exception("You need to set email configs as environment variables")
