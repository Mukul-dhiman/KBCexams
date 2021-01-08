import smtplib 
import config_mail as config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(reciver,message):



    sender = config.MAIL_USERNAME
    password = config.MAIL_PASSWORD

    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = sender 
  
    # storing the receivers email address  
    msg['To'] = reciver 
  
    # storing the subject  
    msg['Subject'] = "KBCexams | Change Password Link"
  
    # string to store the body of the mail 
    body = message

    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    
    # creates SMTP session 
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 

    # start TLS for security 
    smtp.starttls() 

    # Authentication 
    smtp.login(sender, password) 

    text = msg.as_string()
    
    # sending the mail 
    smtp.sendmail(sender, reciver, text) 

    # terminating the session 
    smtp.quit() 
