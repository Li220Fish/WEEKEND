# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 21:17:49 2024

@author: 李魚
"""

from flask import Flask, request, jsonify, render_template , redirect , url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from SQL import DataBase
import UPS #user password setting
import logging
import os , sys
import threading
import time
import chat_model

app = Flask(__name__,static_folder='frontend/build',static_url_path='/')
#app.wsgi_app = ProxyFix(app.wsgi_app)
data_db = DataBase()

global user_list
user_list = []

@app.route('/')
def home(): 
    #user_ip = request.remote_addr
    #logging.debug(user_ip)
    #user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #response = os.system('ping -c 3 -i 1 ' + user_ip)
    #user_list.append(user_ip)
    return app.send_static_file('index.html') #render_template('index.html')

@app.route('/info', methods=['POST'])
def information():
    try:
        data = request.get_json()  # 從 POST 請求中獲取 JSON 資料
        user_id = data.get('id')
        user_name = data_db.find(f"SELECT `User_name` FROM `account` WHERE `ID of Account` ='{user_id}'")[0][0]
        like = data_db.find(f"SELECT COUNT(*) FROM `favorite cocktail` WHERE `ID of Account`='{user_id}';")[0][0]
        comment = data_db.find(f"SELECT COUNT(*) FROM `cocktail of message` WHERE `ID of Account` = '{user_id}'")[0][0]
        if user_id !="" and user_name !="" and like !="":
            return jsonify({'username': user_name ,'like':like,'comment':comment})
    except:
        return jsonify({'message':'稍後在試'})

@app.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()  # 從 POST 請求中獲取 JSON 資料
    print(data)
    username = data.get('email')
    password = data.get('password')
    print(username,password)
    sql = f"SELECT * FROM account WHERE Gmail = '{username}' "
    
    try:
        #print(username,password)
        datas = data_db.find(sql)
        ID = data_db.find("SELECT COUNT(*) FROM `account`;")[0][0] +1
        if ID <10: ID = '0'+str(ID)
        if len(datas) == 1:
            if password == datas[0][3]:
                message = '成功登入!'
                #global page
                #page = 'index.html'
                return jsonify({'message': message ,'user_id':datas[0][0]})
                #return redirect(url_for('/welcome'))
            else:
               message = '密碼錯誤，請再嘗試' 
               return jsonify({'message':message})
        else:
            #sql = f"INSERT INTO `account`(`ID of Account`, `User_name`, `Gmail`, `password`) VALUES ('I{ID}','user_{ID}','{username}','{password}')"
            if username != "" and password != "":
                message = '帳號不存在' 
                return jsonify({'message': message})
            return jsonify({'message': "不可為空"})
    except:
        message = EOFError
        print("出現一點點錯誤")
    return jsonify({'message': message})

@app.route('/forget',methods=['POST'])
def forget():
    data = request.get_json()
    email = data.get('email')  
    new_pass =  UPS.reset_password()
    print(new_pass)
    try:
        sql = f"UPDATE account SET `password` = '{new_pass}' WHERE Gmail='{email}' "
        data_db.insert(sql)
        UPS.send(email, new_pass,1)
    except:
        print("重設密碼錯誤")
    
    return jsonify({'message': 'Email received'}) 

@app.route('/create',methods=['POST'])
def create():
    data = request.get_json()
    email = data.get('email')
    ID = data_db.find("SELECT COUNT(*) FROM `account`;")[0][0] +1
    new_pass =  UPS.reset_password()
    state =  data_db.find(f"SELECT * FROM account WHERE Gmail = '{email}' ")
    print(state,len(state))
    if len(state) == 0:
        
        try:
            sql =f"INSERT INTO `account`(`ID of Account`, `User_name`, `Gmail`, `password`) VALUES ('I{ID}','user_{ID}','{email}','{new_pass}')"
            data_db.insert(sql)
            UPS.send(email, new_pass,2)
        except:
            print("帳戶創建錯誤")
            return jsonify({'message': 'Error!'})
        
        return jsonify({'message': 'create a new account'})
    else:
        return jsonify({'message': '帳號已存在'})

@app.route('/name_save',methods=['POST'])
def name_save():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_id = data.get('id')
    
    sql = f"SELECT * FROM `account` WHERE `password`='{password}' and `ID of Account` ='{user_id}'"
    datas = data_db.find(sql)
    if len(datas) ==1:
        sql = f"UPDATE `account` SET `User_name`='{username}' WHERE `ID of Account` ='{user_id}'"
        data_db.insert(sql)
        return jsonify({'message': '完成'})
    else:
        return jsonify({'message': '錯誤'})

@app.route('/pass_save',methods=['POST'])
def pass_save():
    data = request.get_json()
    
    password_new = data.get('password_new')
    gmail = data.get('gmail')
    password = data.get('password')
    user_id = data.get('id')
    
    sql = f"SELECT * FROM `account` WHERE `password`='{password}' and `ID of Account` ='{user_id}'"
    datas = data_db.find(sql)
    if len(datas) ==1:
        sql = f"UPDATE `account` SET `Gmail`='{gmail}',`password`='{password_new}' WHERE `ID of Account` ='{user_id}'"
        data_db.insert(sql)
        return jsonify({'message': '完成'})
    else:
        return jsonify({'message': '錯誤'})

@app.route('/chat_bot',methods=['POST'])
def chat():
    data = request.get_json().get('message')
    sp = request.get_json().get('Sp')
    print(sp+data)
    re_data = chat_model.chatbot(sp+data)
    print(re_data)
    return jsonify(re_data)


@app.route('/api/cocktails', methods=['GET'])
def get_cocktails():
    try:
        cocktails = data_db.get_cocktail()
        #if 'error' in cocktails:
            #return jsonify({'error': cocktails['error']}), 500
        if not cocktails:
            return jsonify({'message': 'No cocktails found'}), 404
    
        return jsonify(cocktails)
    except:
        print("出了一點點錯")

@app.route('/api/cocktails/<cocktail_id>', methods=['POST'])
def get_cocktail(cocktail_id):
    data = request.get_json()
    user_id = data.get("user_id")
    
    cocktail = data_db.get_cocktail_by_id(cocktail_id,user_id)
    
    if 'error' in cocktail:
        pass

    if not cocktail:
        return jsonify({'message': 'Cocktail not found'}), 404

    return jsonify(cocktail)

@app.route('/api/cocktails/<cocktail_id>/like', methods=['POST'])
def like_cocktail(cocktail_id):
    data = request.get_json()
    action = data.get('action')
    user_id = data.get('user_id')
    if action == 'like':
        result = data_db.update_like_status(cocktail_id, 'like',user_id)
    else:
        result = {'error': 'Invalid action'}
    if 'error' in result:
        return jsonify({'error': result['error']}), 500
    return jsonify(result)

@app.route('/api/cocktails/<cocktail_id>/unlike', methods=['POST'])
def unlike_cocktail(cocktail_id):
    data = request.get_json()
    action = data.get('action')
    user_id = data.get('user_id')
    if action == 'unlike':
        result = data_db.update_like_status(cocktail_id, 'unlike',user_id)
    else:
        result = {'error': 'Invalid action'}
    if 'error' in result:
        return jsonify({'error': result['error']}), 500
    return jsonify(result)

@app.route('/api/cocktails/<cocktail_id>/comment', methods=['POST'])
def add_comment_to_cocktail(cocktail_id):
    message = request.json.get('message')
    user_id = request.json.get('user_id')
    
    user_name = data_db.find(f"SELECT `User_name`  FROM `account` WHERE `ID of Account`='{user_id}'")[0][0]
    
    result = data_db.add_comment(cocktail_id,user_id, message)
    if 'error' in result:
        return jsonify({'error': result['error']}), 500
    return jsonify({"user_name":user_name})

@app.route('/api/cocktails/<cocktail_id>/del_comment', methods=['POST'])
def del_comment_to_cocktail(cocktail_id):
    #print(request.get_json())
    coc_id = request.json.get('coc_id')
    message = request.json.get('message')
    user_id = request.json.get('user_id')
    data_db.insert(f"DELETE FROM `cocktail of message` WHERE `Message` = '{message}' and `ID of Cocktail` = '{coc_id}' and `ID of Account` = '{user_id}'") 
    #print(f"DELETE FROM `cocktail of message` WHERE `Message` = '{message}' and `ID of Cocktail` = '{coc_id}' and `ID of Account` = '{user_id}'")
    return jsonify({"message":"完成"})

@app.route('/api/account_activity/likes', methods=['POST'])
def get_likes_history():
    data = request.get_json()
    user_id = data.get('user_id')
    likes_history = data_db.get_likes_history(user_id)
    if 'error' in likes_history:
        return jsonify({'error': likes_history['error']}), 500
    return jsonify(likes_history)

@app.route('/api/account_activity/comments', methods=['POST'])
def get_comments_history():
    data = request.get_json()
    user_id = data.get('user_id')
    #print("123123123123",user_id)
    comments_history = data_db.get_comments_history(user_id)
    if 'error' in comments_history:
        return jsonify({'error': comments_history['error']}), 500
    return jsonify(comments_history)

@app.route('/api/cocktails/<cocktail_id>/ingredients', methods=['GET'])
def get_cocktail_ingredients(cocktail_id):
    ingredients = data_db.get_cocktail_ingredients(cocktail_id)
    if 'error' in ingredients:
        return jsonify({'error': ingredients['error']}), 500

    if not ingredients:
        return jsonify({'message': 'Ingredients not found'}), 404
    return jsonify(ingredients)

@app.route('/api/most_favorited_cocktails', methods=['GET'])
def most_favorited_cocktails():
    most_favorited = data_db.get_most_favorited_cocktails()
    if 'error' in most_favorited:
        return jsonify({'error': most_favorited['error']}), 500
    cocktails_details = []
    
    for favorite in most_favorited:
        cocktail = data_db.get_cocktail_by_id(favorite['ID of Cocktail'])
        if 'error' in cocktail:
            pass
        cocktails_details.append(cocktail)
        
    return jsonify(cocktails_details)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port = '5000',debug=0)
    #print(chat_model.chatbot("#0我想喝甜的調酒"))
    
    