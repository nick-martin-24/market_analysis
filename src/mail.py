#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:42:24 2019

@author: nickmartin
"""
import os
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

def send_mail(to,subject,body):
    user = os.environ['gmail_user']
    pwd = os.environ['gmail_pass']
    # Open the plain text file whose name is in textfile for reading.
    msg = EmailMessage()
    msg.set_content('{}'.format(body))
    
    # me == the sender's email address
    # you == the recipient's email address
    me = '{}@gmail.com'.format(user)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = to
    
    # Send the message via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(user, pwd)
    s.send_message(msg)
    s.quit()
