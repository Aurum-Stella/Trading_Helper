import smtplib
 


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 
# create message object instance
def send_sequrity_code(num_message, email = None, secur_code = None, name = None):
    msg = MIMEMultipart()
    
    
    message = {
        1: f"Приветсвую {name}! Ваш код для регистрации {str(secur_code)}",
        2: f"Код для сброса Вашего пароля {str(secur_code)} "
    }
    

    # setup the parameters of the message
    password = "mCm42xM3b8v8IWaS"
    msg['From'] = "aurum_stella@ukr.net"
    msg['To'] = email
    msg['Subject'] = "AS_Project"
    
    # add in the message body
    msg.attach(MIMEText(message[num_message], 'plain'))
    
    #create server
    server = smtplib.SMTP_SSL(host='smtp.ukr.net',port=465)
    
    #server.starttls()
    
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    try:
        server.sendmail(msg['From'], msg['To'], msg.as_string())
    except smtplib.SMTPRecipientsRefused:
        from AS_Project_logIn import Info_block
        Info_block(6, msg['To'])

    finally:   
        server.quit()

    print("successfully sent email to %s:" % (msg['To']))

