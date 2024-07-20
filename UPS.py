# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 13:57:33 2024

@author: 李魚
"""

import email.message
import smtplib
import random

def send(user,user_password,mode):
    
    password = "odvw rwnp vbrb yetq" #
    msg=email.message.EmailMessage()
    msg["From"]="li220fish@gmail.com"
    msg["To"]= str(user)#"li220fish@gmail.com" #testing
    print(user)
    if mode == 1:
        msg["Subject"]="重設密碼通知"
        msg.add_alternative(f"已重新更新密碼，密碼為{user_password}",subtype="html") #HTML信件內容
    elif mode == 2:
        msg["Subject"]="創立帳號通知"
        msg.add_alternative(f"歡迎您使用WEEKEND，您的預設密碼為{user_password}",subtype="html") #HTML信件內容
         
    server=smtplib.SMTP_SSL("smtp.gmail.com",465) #建立gmail連驗
    server.login("li220fish@gmail.com",password)
    server.send_message(msg)
    server.close() #發送完成後關閉連線

def reset_password():
    new_pass = ""
    pass_len = ['1','2','3','4','5','6','7','8','9','0','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm','n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M','N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in range(8):
        new_pass += random.choice(pass_len)
    return new_pass


        
