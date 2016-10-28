import smtplib
import email.utils
from email.mime.text import MIMEText
#
import configs



msg_template = "description: %s \n price: %s \n sq ft: %s \n location: %s \n %s\n\n"


def mail(listings):
    """ Compose an email of apartment listings and send to predefined addres """
    # Compose message body
    msg_ = ""
    for value in listings.values():
        msg_ = msg_ + msg_template % (value['description'],value['price'],\
        value["size"],value["location"],value["href"])

    # Create the message object
    msg = MIMEText(msg_)
    msg.set_unixfrom('author')
    msg['To'] = email.utils.formataddr(('Recipient', configs.to_email_address))
    msg['From'] = email.utils.formataddr(('Author', configs.from_email_address))
    msg['Subject'] = 'Freshly squeezed listings'

    server = smtplib.SMTP(configs.from_email_smtpserver, configs.from_email_port)

    try:
        server.set_debuglevel(True)
        server.ehlo()
        # see if session can be encrypted
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo()

        server.login(configs.from_email_address, configs.from_email_pswd)
        server.sendmail(configs.from_email_address, [configs.to_email_address], msg.as_string())
    finally:
        server.quit()
