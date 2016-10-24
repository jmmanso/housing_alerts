###
###
import smtplib
import email.utils
from email.mime.text import MIMEText
import getpass
#
import configs
import special_configs



msg_template = "description: %s \n price: %s \n sq ft: %s \n location: %s \n %s\n\n"


def mail(listings):

    msg_ = ""
    for value in listings.values():
        msg_ = msg_ + msg_template % (value['description'],value['price'],\
        value["size"],value["location"],value["href"])

    # Create the message
    msg = MIMEText(msg_)
    msg.set_unixfrom('author')
    msg['To'] = email.utils.formataddr(('Recipient', configs.to_email))
    msg['From'] = email.utils.formataddr(('Author', configs.from_email))
    msg['Subject'] = 'Freshly squeezed listings'

    server = smtplib.SMTP(configs.email_hostname,configs.email_port)

    try:
        server.set_debuglevel(True)
        # identify ourselves, prompting server for supported features
        server.ehlo()
        # If we can encrypt this session, do it
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo() # re-identify ourselves over TLS connection

        server.login(configs.email_uname, configs.email_pswd)
        server.sendmail(configs.from_email, [configs.to_email], msg.as_string())
    finally:
        server.quit()
