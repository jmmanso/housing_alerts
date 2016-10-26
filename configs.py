import os

cl_search_url = "https://sfbay.craigslist.org/search/sfc/apa?hasPic=1&nh=4&nh=12&nh=18&max_price=2500&bedrooms=1&bathrooms=1&availabilityMode=0"

dolores_search_url240 = "http://www.240doloresapts.com/floorplan/1x1/"
dolores_search_url230 = "http://www.230doloresapts.com/floorplan/1x1/"


thisdir = os.path.dirname(__file__)
cl_dump_json_path = thisdir+"/files/cl_historic.json"
cl_new_json_path = thisdir+"/files/cl_new.json"

email_uname = "alfonso.perez.munoz72@hotmail.com"
email_hostname = "smtp.live.com"
email_port = 587 #25


from_email = email_uname
