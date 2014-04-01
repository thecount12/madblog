#!/usr/bin/python
# mail form program using gmail
import base64
import smtplib
from email.mime.text import MIMEText

# change smtpuser, zap
# recipients I use similar to carbon copy 
# REPLY_TO_ADDRESS is the user filling out the form


def gmail(REPLY_TO_ADDRESS,data,subject):
        smtpserver = 'smtp.gmail.com' # gmail smtp 
        smtpuser = 'user@gmail.com' # gmail user account
        zap='' # enter encoded password
        str(zap)
        smtppass=base64.b64decode(zap)

	RECIPIENTS = ["'blah' <user@yahoo.com>"]

        msg = MIMEText(data)
        msg['Subject'] = subject 
        msg.add_header('reply-to', REPLY_TO_ADDRESS)

        mailServer = smtplib.SMTP('smtp.gmail.com',587) # 587 
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(smtpuser, smtppass)
        mailServer.sendmail(smtpuser,RECIPIENTS,msg.as_string())
        mailServer.close()

if __name__=="__main__":
        REPLY_TO_ADDRESS='user@linuxmail.org'
        data="any message"
        subject="whatever" 
        gmail(REPLY_TO_ADDRESS,data,subject)


