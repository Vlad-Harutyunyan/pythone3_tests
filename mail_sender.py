import smtplib
import config  #here your gmail login and password
import requests 



class Send_Mail () : 
    
    def __init__ (self,subject,msg,mail_reciver) :
        self.sub = subject
        self.msg = msg
        self.mail_reciver = mail_reciver

    def send (self) :
        try : 
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(config.EMAIL_ADDRES,config.EMAIL_PASSWORD) 
            message ='Subject: {}\n\n{}'.format(self.sub,self.msg)
            server.sendmail(self.mail_reciver,self.mail_reciver , message)
            server.quit() 
            print('success email send !!')
            
        except : 
            print('email faild to send !!')



subject = input('Who are you ? : ')
msg = input('What do you say ? : ')
rec = input('Wo are recive your email : ')
Send_Mail(subject,msg,rec).send() 

