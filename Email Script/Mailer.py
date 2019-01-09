import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


# Mailing code taken form Mathieu Germain (mathieu.germain@gmail.com)
# Sends a email (message).
def send_email(message, subject, to, cc=None):
    # create message object instance
    msg = MIMEMultipart()

    # Change based on ICML
    #
    #

    msg['From'] = "NIPS2018<jeshurannips@gmail.com>"
    msg['To'] = to
    msg['Reply-to'] = "jira@nipsworkflow.atlassian.net"
    if cc:
        msg['CC'] = cc
        # msg['CC'] = "nips2018pc@googlegroups.com"
    msg['Subject'] = subject
    # add in the message body
    # TODO: Use HTML email for richer/prettier email.
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()

    # NOTE: How to use AppPassword for google products https://support.google.com/accounts/answer/185833?hl=en
    # NOTE: How to generate AppPassword https://security.google.com/settings/security/apppasswords
    # TODO: This should not be here this should be in a separate config file reat by the script.
    # See https://docs.python.org/3/library/configparser.html
    # No two step so will work with password.
    # You can use just the password by not enabling 2 step in Gmail
    server.login(<email>, <password>)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    time.sleep(1)
    server.quit()
