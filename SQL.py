# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 00:59:45 2024

@author: 李魚
"""
from collections import Counter
from datetime import datetime
import pymysql

class DataBase():
    def connect(self):
        self.conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="weekend2", 
            charset="utf8")
    """
    def connect(self):
        self.conn = pymysql.connect(
            host="172.26.5.123",#,"61.218.122.234"
            user="remote_user",
            password="",
            database="weekend2", 
            charset="utf8")
    """
    def disconnect(self):
        if self.conn:
            self.conn.close()
    def find(self,sql_order, params=None):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql_order, params)
                datas = cursor.fetchall()
            return datas
        except:
            print('資料讀取錯誤')
    def insert(self,sql_oredr):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                
                cursor.execute(sql_oredr)
                
                self.conn.commit()
        except:
            print("資料插入錯誤")
            
    def get_cocktail(self):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                query = ("SELECT `ID of Cocktail`, `ID of Liquor`, `Name of Cocktail`, "
                         "`English Name of Cocktail`, `Production Method`, "
                         "`Low alcohol concentration`, `Medium alcohol concentration`, "
                         "`High alcohol concentration`, `Sour`, `Sweet`, `Bitter`, "
                         "`Spicy`, `Ice`, `Hot` FROM `cocktail list`")
                cursor.execute(query)

                cocktails = []
                for row in cursor.fetchall():
                    # Convert the row to a dictionary
                    cocktail = {
                        'ID of Cocktail': row[0],
                        'ID of Liquor': row[1],
                        'Name of Cocktail': row[2],
                        'English Name of Cocktail': row[3],
                        'Production Method': row[4],
                        'Low alcohol concentration': row[5],
                        'Medium alcohol concentration': row[6],
                        'High alcohol concentration': row[7],
                        'Sour': row[8],
                        'Sweet': row[9],
                        'Bitter': row[10],
                        'Spicy': row[11],
                        'Ice': row[12],
                        'Hot': row[13]
                    }
                    cocktails.append(cocktail)
                    
                cursor.close()

            return cocktails

        except:
            return {'error':"An error occurred while fetching data:"}

    def get_cocktail_by_id(self, cocktail_id,user_id=""):
        self.connect()
        try:
            with self.conn.cursor() as cursor:

                query = (f"SELECT `cocktail list`.`ID of Cocktail`, `ID of Liquor`, `Name of Cocktail`, `English Name of Cocktail`, `Production Method`, `Low alcohol concentration`, `Medium alcohol concentration`, `High alcohol concentration`, `Sour`, `Sweet`, `Bitter`, `Spicy`, `Ice`, `Hot`, `User_name`, `Message`,`time` FROM (`cocktail list` LEFT JOIN `cocktail of message` ON `cocktail list`.`ID of Cocktail` = `cocktail of message`.`ID of Cocktail`) left JOIN `account` ON `cocktail of message`.`ID of Account` = `account`.`ID of Account` WHERE `cocktail list`.`ID of Cocktail` = '{cocktail_id}';")
                cursor.execute(query)
                rows = cursor.fetchall()
                
                if rows:
                    cocktail = {
                        'ID of Cocktail': rows[0][0],
                        'ID of Liquor': rows[0][1],
                        'Name of Cocktail': rows[0][2],
                        'English Name of Cocktail': rows[0][3],
                        'Production Method': rows[0][4],
                        'Low alcohol concentration': rows[0][5],
                        'Medium alcohol concentration': rows[0][6],
                        'High alcohol concentration': rows[0][7],
                        'Sour': rows[0][8],
                        'Sweet': rows[0][9],
                        'Bitter': rows[0][10],
                        'Spicy': rows[0][11],
                        'Ice': rows[0][12],
                        'Hot': rows[0][13],
                        'comments': []
                    }

                    for row in rows:
                        if row[15] is not None:
                            comment = {
                                'User_name': row[14],
                                'Message': row[15],
                                'time': row[16]
                            }
                            cocktail['comments'].append(comment)
                    
                    # Query to count likes
                    likes_query = f"SELECT COUNT(*) FROM `favorite cocktail` WHERE `ID of Cocktail` = '{cocktail_id}'"
                    cursor.execute(likes_query)
                    likes_count = cursor.fetchone()[0]
                    cocktail['likes'] = likes_count

                    # Query to check if liked by 'CSIE'
                    liked_query = f"SELECT COUNT(*) FROM `favorite cocktail` WHERE `ID of Cocktail` = '{cocktail_id}' AND `ID of Account` = '{user_id}'"
                    cursor.execute(liked_query)
                    is_liked = cursor.fetchone()[0] > 0
                    cocktail['is_liked'] = is_liked

                else:
                    cocktail = None

                cursor.close()

            return cocktail
        except:
            return {'error': "An error occurred while updating like status"}
            
        
    def update_like_status(self, cocktail_id, action , user_id):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                if action == 'like':
                    query = (f"INSERT INTO `favorite cocktail` (`ID of Cocktail`, `ID of Account`) VALUES ('{cocktail_id}', '{user_id}')")
                elif action == 'unlike':
                    query = (f"DELETE FROM `favorite cocktail` WHERE `ID of Cocktail` = '{cocktail_id}' AND `ID of Account` = '{user_id}'")
                
                cursor.execute(query)
                self.conn.commit()

            return {'message': 'Success'}
        except:
            return {'error': "An error occurred while updating like status"}
        
    def add_comment(self,cocktail_id, user_id, message):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
                
                query = (f"INSERT INTO `cocktail of message` (`ID of Cocktail`, `ID of Account` ,`Message`, `time`) VALUES ('{cocktail_id}','{user_id}','{message}' ,'{time_now}')")
                print(f"INSERT INTO `cocktail of message` (`ID of Cocktail`, `ID of Account` ,`Message`, `time`) VALUES ('{cocktail_id}','{user_id}','{message}' ,'{time_now}')")
                cursor.execute(query)
                self.conn.commit()
            return {'message': 'Comment added successfully'}
        except:
            return {'error'}

    def get_likes_history(self,user_id):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                query = (f"SELECT `favorite cocktail`.`ID of Cocktail`, `cocktail list`.`Name of Cocktail`, `cocktail list`.`English Name of Cocktail` FROM `favorite cocktail`INNER JOIN `cocktail list` ON `favorite cocktail`.`ID of Cocktail` = `cocktail list`.`ID of Cocktail`WHERE `favorite cocktail`.`ID of Account` = '{user_id}';")
                cursor.execute(query)
                likes = cursor.fetchall()
                cursor.close()
            
            return [{'ID_of_Cocktail': row[0], 'Name_of_Cocktail': row[1], 'English_Name_of_Cocktail': row[2]} for row in likes]
        
        except:
            return {'error': "An error occurred while fetching data"}

    def get_comments_history(self,user_id):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                query = (f"SELECT `cocktail of message`.`ID of Cocktail`, `cocktail list`.`Name of Cocktail`, `cocktail list`.`English Name of Cocktail`, `cocktail of message`.`Message`, `cocktail of message`.`time` FROM `cocktail of message` INNER JOIN `cocktail list` ON `cocktail of message`.`ID of Cocktail` = `cocktail list`.`ID of Cocktail` WHERE `cocktail of message`.`ID of Account` = '{user_id}';")
                cursor.execute(query)
                comments = cursor.fetchall()
                cursor.close()
            
            return [{'ID_of_Cocktail': row[0], 'Name_of_Cocktail': row[1], 'English_Name_of_Cocktail': row[2], 'Message': row[3], 'time': row[4]} for row in comments]
        
        except:
            return {'error': "An error occurred while fetching data"}
        
    def get_cocktail_ingredients(self, cocktail_id):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                query = (f"SELECT `liquor`.`name of wine`, `ingredients of wine`.`Name of Ingredients`,`ingredients of cocktail`.`Amount of Used` FROM `cocktail list` LEFT JOIN `liquor` ON `cocktail list`.`ID of Liquor` = `liquor`.`ID of Liquor` LEFT JOIN `ingredients of cocktail` ON `cocktail list`.`ID of Cocktail` = `ingredients of cocktail`.`ID of Cocktail` LEFT JOIN `ingredients of wine` ON `ingredients of cocktail`.`ID of Ingredients` = `ingredients of wine`.`ID of Ingredients` WHERE `cocktail list`.`ID of Cocktail` = '{cocktail_id}'")

                cursor.execute(query)
                ingredients = cursor.fetchall()
                cursor.close()

            return {
                'name of wine': ingredients[0][0] if ingredients else None,
                'ingredients': [
                    {'Name of Ingredients': row[1], 'Amount of Used': row[2]}
                    for row in ingredients
                ]
            }
        except :
            return {'error': "An error occurred while fetching data"}
    
    def get_cocktail_production_method(self, cocktail_name):
    
        sql ="""
        SELECT `Production Method`
        FROM `cocktail list`
        WHERE `Name of Cocktail` = %s
        """
        records = self.find(sql, (cocktail_name,))
        if records:
            return [record[0] for record in records]
        else:
            return None
        
    def get_most_favorited_cocktails(self):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                query = ("SELECT `ID of Cocktail`, COUNT(*) AS `Duplicate_Count` FROM `favorite cocktail` GROUP BY `ID of Cocktail` HAVING COUNT(*) >= 1 ORDER BY `Duplicate_Count` DESC LIMIT 10;")
                cursor.execute(query)
                favorites = cursor.fetchall()
                cursor.close()
            return [{'ID of Cocktail': row[0], 'Duplicate_Count': row[1]} for row in favorites]
        except:
            return {'error': "An error occurred while fetching data"}
        
    
#data_db = DataBase()
#print(data_db.get_most_favorited_cocktails())

        

        