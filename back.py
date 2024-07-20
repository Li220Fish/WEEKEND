# -*- coding: utf-8 -*-#
"""
Created on Tue Apr 30 01:01:01 2024

@author: 李魚
"""

import pygame as pg
from SQL import DataBase
import TKhelp
import psutil
import random
import sentiment_analysis
import choose_user

data_db = DataBase()
pg.init()
running = True

screen = pg.display.set_mode((900,600))
pg.display.set_caption('manager')
main_clock = pg.time.Clock()

big_font = pg.font.Font("./font/BAHNSCHRIFT.ttf", 72)
mid_font = pg.font.Font("./font/BAHNSCHRIFT.ttf", 56)
title_font = pg.font.Font("./font/BAHNSCHRIFT.ttf", 32)
title2_font = pg.font.Font("./font/TaipeiSansTCBeta.ttf", 28)
inner_font = pg.font.Font("./font/BAHNSCHRIFT.ttf", 20)
table_font = pg.font.Font("./font/TaipeiSansTCBeta.ttf", 18)
show_font = pg.font.Font("./font/BAHNSCHRIFT.ttf", 14)

background = pg.image.load("./image/background.png")
background.set_alpha(150)

speak_list = ['Fat people are more likely to get ','In the UK, you can drink alcohol as','Alcoholic beverages are available at','Alcohol actually lowers your body','Glowing cocktail - Gin Tonic']
speak2_list= ['drunk than thin people','young as 5 years old','McDonald’s in Germany and France','temperature','']


mode = 2; not_in = True ; row_x = 10 ; first = 0 ; counter = 800
account_mode = 1 ; wine_mode = 1 ; cocktail_mode = 1
ingredients_mode = 1 ; fish_mode = 1 ; comment_mode = 1 ; login = 0 
first_run = 1
ana_msg = [] ; ana_per = []


fish_type = [1,1,1,1,1,1]
fish_x = [-50,-50,-50,-50,-50,-50]
fish_y = [-50,-50,-50,-50,-50,-50]
fish_move = [random.choice([1,-1]),random.choice([1,-1]),random.choice([1,-1]),random.choice([1,-1]),random.choice([1,-1]),random.choice([1,-1])]
fish_ran = [0,0,0,0,0,0]
for i in range(6):
    fish_ran[i] = random.choice([1,2,3,-1,-2,-3])


CPU = psutil.cpu_percent() ; RAM = psutil.virtual_memory()[2]

page = [] ; read_page = 0

def top_three_indices(arr):
    # 創建數值及其索引的對應列表
    value_index_pairs = [(value, index) for index, value in enumerate(arr)]
    
    # 根據數值進行排序，降序排列
    value_index_pairs.sort(key=lambda x: x[0], reverse=True)
    
    # 提取前三個元素的索引
    top_three = [index for value, index in value_index_pairs[:3]]
    
    return top_three

datas = data_db.find(" SELECT * FROM `cocktail of message` ")
for i in range(len(datas)): page.append(0)

show = ''

data_x = 180 ; data_y = 150 
while running:
    
    main_clock.tick(24)
    user = pg.mouse.get_pos()
    x = user[0] ;y = user[1] 
    mouse = pg.mouse.get_pressed()
    
    screen.fill((245,245,245))
    pg.draw.rect(screen, (190,190,190), [0,0,900,52],0)
    pg.draw.rect(screen, (255,255,255), [0,0,900,50],0)   
    screen.blit(pg.image.load("./image/mark.jpg"), (18,0))
    screen.blit(title_font.render("WEEKEND", True, (19,49,104)), (85,10))
    pg.draw.rect(screen, (36,45,55), [0,52,170,548],0)
    
    #儀錶板(1)
    if x < 170 and 52 < y < 150:
        screen.blit(inner_font.render("Dashboard", True, (255,255,255)), (10,80))      
        screen.blit(show_font.render("You can find out more", True, (178,203,221)), (15,105))
        screen.blit(show_font.render("about how your site", True, (178,203,221)), (15,125))
        if mouse[0] and counter >12:
            screen.blit(background, (0,0))
            screen.blit(title2_font.render("Loading...", True, (36,45,55)), (410,300))
            pg.display.update()
            mode = 1 ; user_label_list = [0,0,0,0] ; preferences = [0,0,0,0,0,0,0,0,0]
            user_i = data_db.find("SELECT `ID of Account` FROM `account`")
            sql = "SELECT `cocktail list`.`Name of Cocktail`, COUNT(*) AS Count FROM `favorite cocktail`INNER JOIN `cocktail list` ON `favorite cocktail`.`ID of Cocktail` = `cocktail list`.`ID of Cocktail` GROUP BY `cocktail list`.`Name of Cocktail` ORDER BY Count DESC;"
            datas = data_db.find(sql)
            lab_s = ["重酒精","大眾味","獨特口味","無喜好"]
            lab_t = ['Low alcohol concentration','Medium alcohol concentration','High alcohol concentration','Sour','Sweet',
                     'Bitter','Spicy','Ice','Hot']
            Tab_H = ["Low","Med","High","Sour","Sweet","Bitter","Spicy","Ice","Hot"]
            
            for i in range(len(user_i)):
                for j in range(4):
                    if choose_user.assign_user_labels(user_i[i][0],data_db)[0] ==  lab_s[j]:
                        user_label_list[j] += 1
                for j in range(9):
                    for k in range(3):
                        if choose_user.assign_user_labels(user_i[i][0],data_db)[1][k] ==  lab_t[j]:
                            preferences[j] += 1
            counter = 0
    else:
        screen.blit(inner_font.render("Dashboard", True, (255,255,255)), (10,80))
    #帳戶(2)
    if x < 170 and 160 < y < 230:
        screen.blit(inner_font.render("Account", True, (255,255,255)), (10,160))
        screen.blit(show_font.render("User's basic information", True, (178,203,221)), (15,185))
        screen.blit(show_font.render("and making remarks", True, (178,203,221)), (15,205))
        if mouse[0]: mode = 2 ; account_mode =1 ; first =0 ; data_x = 180 ; data_y = 150 ; row_x = 10
    else:
        screen.blit(inner_font.render("Account", True, (255,255,255)), (10,160))
    #酒類(3)
    if x < 170 and 240 < y < 310:
        screen.blit(inner_font.render("Wine List", True, (255,255,255)), (10,240))
        screen.blit(show_font.render("Add or delete various ", True, (178,203,221)), (15,265))
        screen.blit(show_font.render("of alcoholic beverages", True, (178,203,221)), (15,285))
        if mouse[0]: mode = 3 ; wine_mode = 1 ; first =0 ; data_x = 160 ; data_y = 150 ; row_x = 10
    else:
        screen.blit(inner_font.render("Wine List", True, (255,255,255)), (10,240))
    #調酒(4)
    if x < 170 and 320 < y < 390:
        screen.blit(inner_font.render("cocktail list", True, (255,255,255)), (10,320))
        screen.blit(show_font.render("Add or delete various ", True, (178,203,221)), (15,345))
        screen.blit(show_font.render("concoctions", True, (178,203,221)), (15,365))
        if mouse[0]: mode = 4 ; cocktail_mode = 1 ; first =0 ; data_x = 160 ; data_y = 150 ; row_x = 10
    else:
        screen.blit(inner_font.render("cocktail list", True, (255,255,255)), (10,320))
    #食材(5)
    if x < 170 and 400 < y < 470:
        screen.blit(inner_font.render("Ingredients", True, (255,255,255)), (10,400))
        screen.blit(show_font.render("Add or delete drink ", True, (178,203,221)), (15,425))
        screen.blit(show_font.render("ingredients", True, (178,203,221)), (15,445))
        if mouse[0]: mode = 5 ; ingredients_mode = 1 ; first =0 ; data_x = 180 ; data_y = 150 ; row_x = 10
    else:
        screen.blit(inner_font.render("Ingredients", True, (255,255,255)), (10,400))
    #評論(6)
    if x <170 and 480 < y < 550:
        screen.blit(inner_font.render("Comment", True, (255,255,255)), (10,480))
        screen.blit(show_font.render("Add or delete ", True, (178,203,221)), (15,505))
        screen.blit(show_font.render("negative comments", True, (178,203,221)), (15,525))
        if mouse[2]: mode = 6 
        elif mouse[0]: 
            mode = 7 ; first_run = 1 ; comment_mode=1 ; ana_msg = [] ; ana_per = [] 
            page = [] ; read_page = 0 ; first = 0
            datas = data_db.find(" SELECT * FROM `cocktail of message` ")
            for i in range(len(datas)): page.append(0)
    else:
        screen.blit(inner_font.render("Comment", True, (255,255,255)), (10,480))
    
    screen.blit(show_font.render("__________________________", True, (178,203,221)), (5,549))
    screen.blit(show_font.render("Power By 8_8fish", True, (178,203,221)), (20,570))
    
    if mode == 0:
        #main_clock.tick(10)
        
        counter += 1
        screen.fill((255,255,255))
        screen.blit(pg.image.load("./image/key.png"), (0,0))
        
        screen.blit(pg.image.load("./image/logo.jpg"), (375,60))
        screen.blit(big_font.render("WEEKEND", True, (19,49,104)), (521,77))
        screen.blit(title_font.render("Do you know?", True, (36,45,55)), (380,177))
        screen.blit(title2_font.render(f'{show}', True, (233,138,121)), (530,430))
        
        if counter < 1280:
            #print(counter)
            s = speak_list[(counter//256)]
            s2 = speak2_list[(counter//256)]
            screen.blit(title2_font.render(f"{s}", True, (36,45,55)), (400,227))
            screen.blit(title2_font.render(f"{s2}", True, (36,45,55)), (400,267))
        else:
            counter = 0
            
        if 520 < x < 770 and 470 < y <520 and not_in: # login
            pg.draw.rect(screen, (36,45,55), [505,470,250,50],0)
            screen.blit(title_font.render("GET START", True, (255,255,255)), (555,480))
            if mouse[0] and counter > 12 : 
                counter = 100 ; login = 1
        else:
            pg.draw.rect(screen, (226,226,226), [505,470,250,50],0)
            screen.blit(title_font.render("GET START", True, (0,0,0)), (555,480))
        
        if login == 1:
            try:
                show = TKhelp.login_from()
                if show == '    Correct':
                    for i in range(375,875,5):
                        main_clock.tick(30)
                        pg.draw.rect(screen, (0,0,0), [i,550,5,5],0)
                        pg.display.update()
                    
                    mode = 1 ; user_label_list = [0,0,0,0] ; preferences = [0,0,0,0,0,0,0,0,0]
                    user_i = data_db.find("SELECT `ID of Account` FROM `account`")
                    sql = "SELECT `cocktail list`.`Name of Cocktail`, COUNT(*) AS Count FROM `favorite cocktail`INNER JOIN `cocktail list` ON `favorite cocktail`.`ID of Cocktail` = `cocktail list`.`ID of Cocktail` GROUP BY `cocktail list`.`Name of Cocktail` ORDER BY Count DESC;"
                    datas = data_db.find(sql)
                    lab_s = ["重酒精","大眾味","獨特口味","無喜好"]
                    lab_t = ['Low alcohol concentration','Medium alcohol concentration','High alcohol concentration','Sour','Sweet',
                             'Bitter','Spicy','Ice','Hot']
                    Tab_H = ["Low","Med","High","Sour","Sweet","Bitter","Spicy","Ice","Hot"]
                    
                    for i in range(len(user_i)):
                        for j in range(4):
                            if choose_user.assign_user_labels(user_i[i][0],data_db)[0] ==  lab_s[j]:
                                user_label_list[j] += 1
                        for j in range(9):
                            for k in range(3):
                                if choose_user.assign_user_labels(user_i[i][0],data_db)[1][k] ==  lab_t[j]:
                                    preferences[j] += 1   
            except:
                show = "       Try Again"
            login = 0
        
    if mode == 1:
        counter += 1 ; 
        
        if counter > 60:
            CPU = psutil.cpu_percent() ; RAM = psutil.virtual_memory()[2]
            counter = 0
        
        screen.blit(inner_font.render("Dashboard", True, (43,192,109)), (10,80))
        screen.blit(show_font.render("You can find out more", True, (178,203,221)), (15,105))
        screen.blit(show_font.render("about how your site", True, (178,203,221)), (15,125))
        #top
        pg.draw.rect(screen, (255,255,255), [200,80,670,200],0)
        pg.draw.rect(screen, (226,226,226), [225,240,320,3],0)
        
        screen.blit(table_font.render("重酒精", True, (0,0,0)), (235,248))
        screen.blit(table_font.render("大眾味", True, (0,0,0)), (310,248))
        screen.blit(table_font.render("獨特口味", True, (0,0,0)), (385,248))
        screen.blit(table_font.render("無喜好", True, (0,0,0)), (480,248))
        
        screen.blit(title_font.render("User Label", True, (36,45,55)), (300,90))
        
        
        for i in range(4):
            per_h = int((user_label_list[i]/len(user_i))*100) #per_h = int((user_label_list[0]/len(user_i))*100) 原本len用超過長度
            if per_h != 0:
                if i == 0:
                    pg.draw.rect(screen, (233,138,121), [243,230-int(1.3*per_h),40,(240-int(230-int(1.3*per_h)))],0)  
                elif i == 1:
                    pg.draw.rect(screen, (233,138,121), [318,230-int(1.3*per_h),40,(240-int(230-int(1.3*per_h)))],0)  
                elif i == 2:
                    pg.draw.rect(screen, (233,138,121), [400,230-int(1.3*per_h),40,(240-int(230-int(1.3*per_h)))],0)  
                elif i == 3:
                    pg.draw.rect(screen, (233,138,121), [488,230-int(1.3*per_h),40,(240-int(230-int(1.3*per_h)))],0)  
        
        screen.blit(title_font.render("Preferences", True, (36,45,55)), (630,90))
        bu_x = 630 ; bu_y = 150
        for i in range(1,10): 
            if i in top_three_indices(preferences):
                color = (36,45,55)
            else:
                color = (226,226,226)
            screen.blit(inner_font.render(f"{Tab_H[i-1]}", True, color), (bu_x,bu_y))

            if not(i % 3):
                bu_x = 630 ; bu_y += 40 
            else:
                bu_x += 70 
        
        #left
        pg.draw.rect(screen, (255,255,255), [200,300,470,280],0)
        screen.blit(title_font.render("Ranking List", True, (36,45,55)), (210,310))
        
        
        for i in [420,500]: pg.draw.line(screen, (226,226,226), (210,i), (660,i),2)
        try:
            for i in range(1,4): 
                screen.blit(title_font.render(f"{i}", True, (36,45,55)), (220,300+75*i))
                screen.blit(title2_font.render(f"{datas[i-1][0]}", True, (36,45,55)), (260,300+75*i))
                screen.blit(title_font.render(f"{str(datas[i-1][1])}", True, (36,45,55)), (630,300+75*i))
        except:
            pass
    
        #right
        
        pg.draw.rect(screen, (255,255,255), [700,300,170,280],0)
        screen.blit(title_font.render("CPU", True, (36,45,55)), (710,310))
        pg.draw.rect(screen, (245,245,245), [725,420,120,3],0)
        pg.draw.rect(screen, (245,245,245), [725,550,120,3],0)
        if CPU < 50:
            screen.blit(mid_font.render(f"{CPU}", True, (36,45,55)), (735,355))
            pg.draw.rect(screen, (36,45,55), [725,420,int(CPU*1.2),3],0)
        else:
            screen.blit(mid_font.render(f"{CPU}", True, (230,0,0)), (735,355))
            pg.draw.rect(screen, (230,0,0), [725,420,int(CPU*1.2),3],0)
            
        screen.blit(title_font.render("RAM", True, (36,45,55)), (710,440))
        if RAM < 80:
            screen.blit(mid_font.render(f"{RAM}", True, (36,45,55)), (735,485))
            pg.draw.rect(screen, (36,45,55), [725,550,int(RAM*1.2),3],0)
        else:
            screen.blit(mid_font.render(f"{RAM}", True, (230,0,0)), (735,485))
            pg.draw.rect(screen, (230,0,0), [725,550,int(RAM*1.2),3],0)
        
    if mode == 2:# Account
        screen.blit(inner_font.render("Account", True, (43,192,109)), (10,160))
        screen.blit(show_font.render("User's basic information", True, (178,203,221)), (15,185))
        screen.blit(show_font.render("and making remarks", True, (178,203,221)), (15,205))
        if account_mode == 1:#show所有帳號
            counter += 1
            screen.blit(title_font.render("Account Basic", True, (36,45,55)), (180,65))
            data_x = 180 ; data_y = 150 ; counter += 1
            datas = data_db.find(" SELECT `ID of Account`,`User_name`,`Gmail` FROM `account` ")
            pg.draw.rect(screen, (226,226,226), [180,110,700,30],0)
            if first+row_x >= len(datas): row_x = len(datas) - first 
            else: row_x = 10
            #table desgin
            screen.blit(inner_font.render("ID of Account", True, (0,0,0)), (190,115))
            screen.blit(inner_font.render("User Name", True, (0,0,0)), (350,115))
            screen.blit(inner_font.render("User Gmail", True, (0,0,0)), (520,115))
            s = 0
            for i in range(first,first+row_x):
                if data_x < x and data_y+30*s < y < data_y+30*(s+1): 
                    color = (233,138,121)
                    if mouse[0] and counter > 12: 
                        account_id = datas[i][0] ;a_i = i; account_mode =2
                else:
                    color = (0,0,0)
                try:
                    screen.blit(table_font.render(f"{datas[i][0]}", True, color), (data_x+40,data_y+30*s))
                    screen.blit(table_font.render(f"{datas[i][1]}", True, color), (data_x+190,data_y+30*s))
                    screen.blit(table_font.render(f"{datas[i][2]}", True, color), (data_x+340,data_y+30*s))
                except:
                    pass
                s+= 1
            if first > -1 and first+row_x < len(datas):
                if 760 < x < 830 and 530 < y <560 and not_in: # 下一頁
                    pg.draw.rect(screen, (233,138,121), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (255,255,255)), (775,535))
                    if mouse[0] and counter > 12 : 
                        first +=10 ; counter = 0 ;  data_x = 180 ; data_y = 150 ; row_x = 10
                else:
                    pg.draw.rect(screen, (226,226,226), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (0,0,0)), (775,535))
            if first > 0:
                if 180 < x < 250 and 530 < y <560: # 上一頁
                    pg.draw.rect(screen, (233,138,121), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (255,255,255)), (195,535))
                    if mouse[0] and counter > 12 : 
                        first -=10 ; counter = 0 ;  data_x = 180 ; data_y = 150
                else:
                    pg.draw.rect(screen, (226,226,226), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (0,0,0)), (195,535))
        
        if account_mode == 2: #帳號所有留言
            data_x = 210 ; data_y = 350 ; counter +=1
            color = (0,0,0) ; user_label = choose_user.assign_user_labels(datas[a_i][0], data_db)[0]
            screen.blit(title_font.render("Account Advanced", True, (36,45,55)), (180,65))
            pg.draw.rect(screen, (255,255,255), [200,110,150,180],0)
            screen.blit(title_font.render("? ? ? ? ? ? ?", True, (0,0,0)), (210,120))
            screen.blit(title_font.render("? ? ? ? ? ? ?", True, (0,0,0)), (215,160))
            screen.blit(title_font.render("? ? ? ? ? ? ?", True, (0,0,0)), (205,200))
            screen.blit(title_font.render("? ? ? ? ? ? ?", True, (0,0,0)), (210,240))
            screen.blit(title2_font.render(f"ID: {datas[a_i][0]}", True, color), (370,120))
            screen.blit(title2_font.render(f"User Name: {datas[a_i][1]}", True, color), (370,170))
            screen.blit(title2_font.render(f"Gmail: {datas[a_i][2]}", True, color), (370,220))
            screen.blit(title2_font.render(f"Label: {user_label}", True, color), (370,270))
            
            if 780 < x < 850 and 120 < y <150:
                pg.draw.rect(screen, (233,138,121), [780,120,70,30],0)
                screen.blit(inner_font.render("Delete", True, (255,255,255)), (785,125))
                if mouse[0]: account_mode = 4
            else:
                pg.draw.rect(screen, (226,226,226), [780,120,70,30],0)
                screen.blit(inner_font.render("Delete", True, (0,0,0)), (785,125))
            
            pg.draw.rect(screen, (226,226,226), [200,310,650,30],0)
            screen.blit(inner_font.render("Name", True, (0,0,0)), (210,315))
            screen.blit(inner_font.render("Message", True, (0,0,0)), (400,315))
            screen.blit(inner_font.render("time", True, (0,0,0)), (750,315))
            data = data_db.find(f" SELECT `cocktail list`.`ID of Cocktail`, `Name of Cocktail`,`Message`,`time` FROM `cocktail of message`,`cocktail list`,`account` WHERE `cocktail of message`.`ID of Cocktail` = `cocktail list`.`ID of Cocktail` and `cocktail of message`.`ID of Account` = `account`.`ID of Account` and `account`.`ID of Account` = '{account_id}'; ")
            #print(first)
            if first+row_x >= len(data): row_x = len(data) - first 
            else: row_x = 5
            s = 0
            for i in range(first,first+row_x):
                if data_x < x and data_y+30*s < y < data_y+30*(s+1) and x <700: 
                    color2 = (233,138,121)
                    if mouse[0]: 
                        a_i = i; account_mode =3
                        account_msg = data[a_i][2]
                        
                else:
                    color2 = (0,0,0)   
                    
                screen.blit(table_font.render(f"{data[i][1]}", True, color2), (data_x,data_y+30*s))
                screen.blit(table_font.render(f"{data[i][2]}", True, color2), (data_x+190,data_y+30*s))
                screen.blit(table_font.render(f"{data[i][3]}", True, color2), (data_x+490,data_y+30*s))
                s+=1
        
            if first > -1 and first+row_x < len(data):
                if 760 < x < 830 and 530 < y <560 and not_in: # 下一頁
                    pg.draw.rect(screen, (233,138,121), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (255,255,255)), (775,535))
                    if mouse[0] and counter > 12 : 
                        first +=5 ; counter = 0 ;  data_x = 210 ; data_y = 350
                else:
                    pg.draw.rect(screen, (226,226,226), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (0,0,0)), (775,535))
            if first > 0:
                if 180 < x < 250 and 530 < y <560: # 上一頁
                    pg.draw.rect(screen, (233,138,121), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (255,255,255)), (195,535))
                    if mouse[0] and counter > 12 : 
                        first -=5 ; counter = 0 ;  data_x = 210 ; data_y = 350
                else:
                    pg.draw.rect(screen, (226,226,226), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (0,0,0)), (195,535))
    
        if account_mode == 3: #刪除留言
            screen.blit(background, (0,0))
            pg.draw.rect(screen, (255,255,255), [380,190,280,200],0)
            screen.blit(title2_font.render("是否刪除該言論?", True, (36,45,55)), (400,200))
            if 420 < x < 460 and 300 < y < 340:
                screen.blit(title2_font.render("是", True, (233,138,121)), (420,300))
                if mouse[0]: 
                    data_db.insert(f"DELETE FROM `cocktail of message` WHERE `Message` = '{account_msg}' and `ID of Cocktail` = '{data[a_i][0]}'")            
                    account_mode = 2
            else:
                screen.blit(title2_font.render("是", True, (190,190,190)), (420,300))
            
            if 580 < x < 620 and 300 < y < 340:
                screen.blit(title2_font.render("否", True, (233,138,121)), (580,300))
                if mouse[0]: account_mode = 2
            else:
                screen.blit(title2_font.render("否", True, (190,190,190)), (580,300))
            
        if account_mode == 4: #刪除帳號
            screen.blit(background, (0,0))
            pg.draw.rect(screen, (255,255,255), [380,190,280,200],0)
            screen.blit(title2_font.render("是否刪除該帳號?", True, (36,45,55)), (400,200))
            if 420 < x < 460 and 300 < y < 340:
                screen.blit(title2_font.render("是", True, (233,138,121)), (420,300))
                if mouse[0]: 
                    data_db.insert(f" DELETE FROM `account` WHERE `ID of Account` = '{account_id}'")            
                    account_mode = 1
            else:
                screen.blit(title2_font.render("是", True, (190,190,190)), (420,300))
            
            if 580 < x < 620 and 300 < y < 340:
                screen.blit(title2_font.render("否", True, (233,138,121)), (580,300))
                if mouse[0]: account_mode = 2
            else:
                screen.blit(title2_font.render("否", True, (190,190,190)), (580,300))
            
    if mode == 3:#Wine List
        screen.blit(inner_font.render("Wine List", True, (43,192,109)), (10,240))
        screen.blit(show_font.render("Add or delete various ", True, (178,203,221)), (15,265))
        screen.blit(show_font.render("of alcoholic beverages", True, (178,203,221)), (15,285))
        if wine_mode == 1:
            data_x = 160 ; data_y = 150 ; counter +=1
            screen.blit(title_font.render("Wine Basic", True, (36,45,55)), (180,65))
            datas = data_db.find(" SELECT * FROM `wine list` ")
            pg.draw.rect(screen, (226,226,226), [180,110,700,30],0)
            #table desgin
            screen.blit(inner_font.render("ID", True, (0,0,0)), (205,115))
            screen.blit(inner_font.render("Name", True, (0,0,0)), (340,115))
            screen.blit(inner_font.render("Alcohol", True, (0,0,0)), (550,115))
            screen.blit(inner_font.render("Price", True, (0,0,0)), (720,115))
            
            if first+row_x >= len(datas): row_x = len(datas) - first 
            else: row_x = 10
            #print("datas=>" + str(len(datas)) , "first+row_x=>" + first+row_x)
            s = 0
            for i in range(first,first+row_x):
                if data_x < x and data_y+30*s < y < data_y+30*(s+1) and x <750 : 
                    color = (233,138,121)
                    if mouse[0]: 
                        a_i = i; wine_mode =2
                        wine_type = data_db.find(f"SELECT `name of wine` FROM `liquor` WHERE `ID of Liquor` = '{datas[i][0]}'")
                        wine_list = ['ID:','Name:','English Name:','Alchol:','Origin:','Capacity(ml):','price(TWD):']
                else:
                    color = (0,0,0)
                    
                screen.blit(table_font.render(f"{datas[i][1]}", True, color), (data_x+40,data_y+30*s))
                screen.blit(table_font.render(f"{datas[i][2]}", True, color), (data_x+160,data_y+30*s))
                screen.blit(table_font.render(f"{datas[i][4]}", True, color), (data_x+400,data_y+30*s))
                screen.blit(table_font.render(f"{datas[i][7]}", True, color), (data_x+570,data_y+30*s))
                s+=1
            
            if 810 < x < 880 and 170 < y <200: # 新增酒品
                pg.draw.rect(screen, (233,138,121), [810,170,70,30],0)
                screen.blit(inner_font.render("Add", True, (255,255,255)), (828,175))
                if mouse[0]: 
                    wine_mode = 5
            else:
                pg.draw.rect(screen, (226,226,226), [810,170,70,30],0)
                screen.blit(inner_font.render("Add", True, (0,0,0)), (828,175))
            
            if first > -1 and first+row_x < len(datas):
                if 760 < x < 830 and 530 < y <560 and not_in: # 下一頁
                    pg.draw.rect(screen, (233,138,121), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (255,255,255)), (775,535))
                    if mouse[0] and counter > 12 : 
                        first +=10 ; counter = 0 ; data_x = 160 ; data_y = 150
                else:
                    pg.draw.rect(screen, (226,226,226), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (0,0,0)), (775,535))
            if first > 0:
                if 180 < x < 250 and 530 < y <560: # 上一頁
                    pg.draw.rect(screen, (233,138,121), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (255,255,255)), (195,535))
                    if mouse[0] and counter > 12 : 
                        first -=10 ; counter = 0 ;  data_x = 180 ; data_y = 150
                else:
                    pg.draw.rect(screen, (226,226,226), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (0,0,0)), (195,535))
        
        if wine_mode == 2:
            datas = data_db.find(" SELECT * FROM `wine list` ")
            screen.blit(title_font.render("Wine Advanced", True, (36,45,55)), (180,65))
            pg.draw.rect(screen, (226,226,226), [180,110,650,30],0)
            data_x = 210 ; data_y = 350 ; first =0
            screen.blit(title2_font.render(f"{datas[a_i][2]}", True, (0,0,0)), (180,150))
            screen.blit(table_font.render(f"Liquor: {wine_type[0][0]} ", True, (0,0,0)), (180,200))
            for i in range(1,8): screen.blit(table_font.render(f"{wine_list[i-1]} {datas[a_i][i]}", True, (0,0,0)), (180,200+30*i))
            
            if 760 < x < 830 and 220 < y <250: # 修改內容
                pg.draw.rect(screen, (233,138,121), [760,220,70,30],0)
                screen.blit(inner_font.render("Change", True, (255,255,255)), (762,225))
                if mouse[0]: 
                    wine_mode = 3 ; wine_id = datas[a_i][1]
            else:
                pg.draw.rect(screen, (226,226,226), [760,220,70,30],0)
                screen.blit(inner_font.render("Change", True, (0,0,0)), (762,225))
                
            if 760 < x < 830 and 170 < y <200: # 刪除酒品
                pg.draw.rect(screen, (233,138,121), [760,170,70,30],0)
                screen.blit(inner_font.render("Delete", True, (255,255,255)), (765,175))
                if mouse[0]: wine_mode = 4 ; wine_id = datas[a_i][1]
            else:
                pg.draw.rect(screen, (226,226,226), [760,170,70,30],0)
                screen.blit(inner_font.render("Delete", True, (0,0,0)), (765,175))
        
        if wine_mode == 3:
            print(datas[a_i])
            #name, english_name, alcohol, origin, capacity, price = TKhelp.wine_form()
            try:
                name, english_name, alcohol, origin, capacity, price = TKhelp.wine_form(datas[a_i][2],datas[a_i][3],datas[a_i][4],datas[a_i][5],datas[a_i][6],datas[a_i][7])
                #print(f"UPDATE `wine list` SET `Price (TWD)`='{price}'  WHERE `ID of WIne Types` = '{wine_id}'")
                if name != "":   data_db.insert(f"UPDATE `wine list` SET `Name of WIne Types`='{name}'  WHERE `ID of WIne Types` = '{wine_id}'")
                if english_name != "": data_db.insert(f"UPDATE `wine list` SET `Englisg Name of WIne Types`='{english_name}'  WHERE `ID of WIne Types` = '{wine_id}'")
                if alcohol != "": data_db.insert(f"UPDATE `wine list` SET `Alcohol concentration`='{alcohol}'  WHERE `ID of WIne Types` = '{wine_id}'")
                if origin != "": data_db.insert(f"UPDATE `wine list` SET `Origin`='{origin}'  WHERE `ID of WIne Types` = '{wine_id}'")
                if capacity !="": data_db.insert(f"UPDATE `wine list` SET `Capacity(ml)`='{capacity}'  WHERE `ID of WIne Types` = '{wine_id}'")
                if price != "": data_db.insert(f"UPDATE `wine list` SET `Price (TWD)`='{price}'  WHERE `ID of WIne Types` = '{wine_id}'")
                
            except:
                pass
            wine_mode = 2
            
        if wine_mode == 4:
            screen.blit(background, (0,0))
            pg.draw.rect(screen, (255,255,255), [380,190,280,200],0)
            screen.blit(title2_font.render("是否刪除該酒品?", True, (36,45,55)), (410,200))
            if 420 < x < 460 and 300 < y < 340:
                screen.blit(title2_font.render("是", True, (233,138,121)), (420,300))
                if mouse[0]: 
                    data_db.insert(f" DELETE FROM `wine list` WHERE `ID of WIne Types` = '{wine_id}'")            
                    wine_mode = 1
            else:
                screen.blit(title2_font.render("是", True, (190,190,190)), (420,300))
            
            if 580 < x < 620 and 300 < y < 340:
                screen.blit(title2_font.render("否", True, (233,138,121)), (580,300))
                if mouse[0]: wine_mode = 2
            else:
                screen.blit(title2_font.render("否", True, (190,190,190)), (580,300))
            
        if wine_mode == 5:
            datas = data_db.find(" SELECT * FROM `wine list` ")
            try:
                new_id = int(datas[len(datas)-1][1][1:])+1
                if new_id < 10: new_id = f'B0{new_id}'
                else: new_id = f'B{new_id}'
                opts, name, english_name, alcohol, origin, capacity, price = TKhelp.wine_add()
                if name !="": data_db.insert(f"INSERT INTO `wine list`(`Liquor ID`, `ID of WIne Types`, `Name of WIne Types`, `Englisg Name of WIne Types`, `Alcohol concentration`, `Origin`, `Capacity(ml)`, `Price (TWD)`) VALUES ('{opts}','{new_id}','{name}','{english_name}','{alcohol}','{origin}','{capacity}','{price}')")
                row_x = 10 ; 
            except:
                pass #資料尚未完全輸入
            wine_mode = 1
            
    if mode == 4:
        #print(cocktail_mode)
        screen.blit(inner_font.render("cocktail list", True, (43,192,109)), (10,320))
        screen.blit(show_font.render("Add or delete various ", True, (178,203,221)), (15,345))
        screen.blit(show_font.render("concoctions", True, (178,203,221)), (15,365))
        
        if cocktail_mode == 1:
            screen.blit(title_font.render("Cocktail Basic", True, (36,45,55)), (180,65))
            counter += 1
            datas = data_db.find(" SELECT * FROM `cocktail list` ")
            pg.draw.rect(screen, (226,226,226), [180,110,700,30],0)
            #table desgin
            screen.blit(inner_font.render("ID", True, (0,0,0)), (205,115))
            screen.blit(inner_font.render("Name", True, (0,0,0)), (340,115))
            screen.blit(inner_font.render("Label", True, (0,0,0)), (520,115))
            if first+row_x >= len(datas): row_x = len(datas) - first 
            else: row_x = 10
            t = 0
            for i in range(first,first+row_x):
                
                if data_x < x and data_y+30*t < y < data_y+30*(t+1) and x < 800: 
                    color = (233,138,121)
                    if mouse[0]: 
                        #print(len(datas[i]))
                        a_i = i; cocktail_mode =2 ;coc_table = [0,0,0,0,0,0,0,0,0]
                        cocktail_type = data_db.find(f"SELECT `Name of Cocktail` FROM `cocktail list` WHERE `ID of Cocktail` = '{datas[i][0]}'")
                        wine_list = ['ID:','Name:','English Name:','Alchol:','Origin:','Capacity(ml):','price(TWD):']
                else:
                    color = (0,0,0)
                
                screen.blit(table_font.render(f"{datas[i][0]}", True, color), (data_x+40,data_y+30*t))
                screen.blit(table_font.render(f"{datas[i][2]}", True, color), (data_x+160,data_y+30*t))
                table_list = ["","","","","","Low","Med","High","Sour","Sweet","Bitter","Spicy","Ice","Hot"]
                s = 0
                for j in range(5,13): 
                    
                    if str(datas[i][j]) == "1": 
                        
                        screen.blit(table_font.render(f"{table_list[j]}", True, color), (data_x+370 + 80 * s,data_y+30*t)) ; s += 1
                        
                t += 1
                
            if 810 < x < 880 and 170 < y <200: # 新增材料
                pg.draw.rect(screen, (233,138,121), [810,170,70,30],0)
                screen.blit(inner_font.render("Add", True, (255,255,255)), (828,175))
                if mouse[0]: 
                    cocktail_mode = 8
            else:
                pg.draw.rect(screen, (226,226,226), [810,170,70,30],0)
                screen.blit(inner_font.render("Add", True, (0,0,0)), (828,175))
                
            if first > -1 and first+row_x < len(datas):
                if 760 < x < 830 and 530 < y <560 and not_in: # 下一頁
                    pg.draw.rect(screen, (233,138,121), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (255,255,255)), (775,535))
                    if mouse[0] and counter > 12 : 
                        first +=10 ; counter = 0 ;  data_x = 160 ; data_y = 150
                else:
                    pg.draw.rect(screen, (226,226,226), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (0,0,0)), (775,535))
            if first > 0:
                if 180 < x < 250 and 530 < y <560: # 上一頁
                    pg.draw.rect(screen, (233,138,121), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (255,255,255)), (195,535))
                    if mouse[0] and counter > 12 : 
                        first -=10 ; counter = 0 ;  data_x = 160 ; data_y = 150
                else:
                    pg.draw.rect(screen, (226,226,226), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (0,0,0)), (195,535))
        
        if cocktail_mode == 2:
            datas = data_db.find(" SELECT * FROM `cocktail list` ")
            liquor_list = ['Vodka', 'Rum', 'Brandy', 'Liqeur','Gin','Tequila','Wiskey']
            liq_num = int(datas[a_i][1][2])-1
            screen.blit(title_font.render("Cocktail Advanced", True, (36,45,55)), (180,65))
            pg.draw.rect(screen, (226,226,226), [180,110,650,30],0)
            data_x = 210 ; data_y = 350 ; first =0 ; del_item = 0
            screen.blit(title2_font.render(f"{datas[a_i][2]}", True, (0,0,0)), (180,150))
            screen.blit(table_font.render(f"ID : {datas[a_i][0]}", True, (0,0,0)), (180,200))
            screen.blit(table_font.render(f"Liquor : {liquor_list[liq_num]}", True, (0,0,0)), (280,200))
            screen.blit(table_font.render(f"English Name : {datas[a_i][3]}", True, (0,0,0)), (180,230))
            screen.blit(table_font.render("Production Method : ", True, (0,0,0)), (180,260))
            data_x = 200 ; data_y = 290
            coc_text = datas[a_i][4][5:]
            #print(datas[a_i][4][:5]+"s")
            for i in range(4,len(datas[a_i][4])):
                
                if datas[a_i][4][i] == "。": data_x = 200 ; data_y += 30
                else: screen.blit(table_font.render(f"{datas[a_i][4][i]}", True, (0,0,0)), (data_x,data_y)) ; data_x += 18
            
            screen.blit(table_font.render("Table : ", True, (0,0,0)), (180,500))
            s = 0
            for j in range(5,13): 
                coc_table[j-5] = str(datas[a_i][j])
                if str(datas[a_i][j])== "1": 
                    screen.blit(table_font.render(f"{table_list[j]}", True, (0,0,0)), (200 + 80 * s,530)) ; s += 1
            
            if 760 < x < 830 and 220 < y <250: # 修改內容
                pg.draw.rect(screen, (233,138,121), [760,220,70,30],0)
                screen.blit(inner_font.render("Change", True, (255,255,255)), (762,225))
                if mouse[0]: cocktail_mode = 4 ; cocktail_id = datas[a_i][0] ; table_list2 = ['`Low alcohol concentration`','`Medium alcohol concentration`','`High alcohol concentration`','`Sour`','`Sweet`','`bitter`','`spicy`','`Ice`','`Hot`']
            else:
                pg.draw.rect(screen, (226,226,226), [760,220,70,30],0)
                screen.blit(inner_font.render("Change", True, (0,0,0)), (762,225))
                
            if 760 < x < 830 and 170 < y <200: # 刪除酒品
                pg.draw.rect(screen, (233,138,121), [760,170,70,30],0)
                screen.blit(inner_font.render("Delete", True, (255,255,255)), (765,175))
                if mouse[0]: cocktail_mode = 6 ; cocktail_id = datas[a_i][0]
            else:
                pg.draw.rect(screen, (226,226,226), [760,170,70,30],0)
                screen.blit(inner_font.render("Delete", True, (0,0,0)), (765,175))
            
            if 760 < x < 830 and 530 < y <560 and not_in: # 下一頁
                pg.draw.rect(screen, (233,138,121), [760,530,70,30],0)
                screen.blit(inner_font.render("Next", True, (255,255,255)), (775,535))
                if mouse[0]: cocktail_mode = 3 ; cocktail_id = datas[a_i][0]
            else:
                pg.draw.rect(screen, (226,226,226), [760,530,70,30],0)
                screen.blit(inner_font.render("Next", True, (0,0,0)), (775,535))
                
        if cocktail_mode == 3:
            datas = data_db.find(f"SELECT `Name of Ingredients` ,`Amount of used` FROM `ingredients of cocktail` , `ingredients of wine` WHERE `ingredients of cocktail`.`ID of Ingredients` = `ingredients of wine`.`ID of Ingredients` and `ingredients of cocktail`.`ID of Cocktail` = '{cocktail_id}';")
            data_ID = data_db.find(f"SELECT `ingredients of cocktail`.`ID of Ingredients` FROM `ingredients of cocktail` , `ingredients of wine` WHERE `ingredients of cocktail`.`ID of Ingredients` = `ingredients of wine`.`ID of Ingredients` and `ingredients of cocktail`.`ID of Cocktail` = '{cocktail_id}';")
            sel_data = [] 
            screen.blit(title_font.render("Cocktail Advanced", True, (36,45,55)), (180,65))
            pg.draw.rect(screen, (226,226,226), [180,110,650,30],0)
            screen.blit(table_font.render("ingredients of cocktail : ", True, (0,0,0)), (180,150))
            data_x = 200 ; data_y = 180
            
            for i in range(len(datas)): 
                if i < 10:
                    if data_y + 30*i < y < data_y + 30*(i+1) and x < 550: 
                        color = (233,138,121)
                        if mouse[0]:  cocktail_mode = 6 ; del_item = 1 ; ing_id = data_ID[i][0]
                    else: color = (0,0,0)
                    screen.blit(table_font.render(f"{datas[i][0]}", True, color), (data_x,data_y + 30*i)) ; screen.blit(table_font.render(f"{datas[i][1]}", True, color), (400,data_y + 30*i))
                else:
                    if data_y < y < data_y + 30*i and x > 500: color = (233,138,121)
                    else: color = (0,0,0)
                    screen.blit(table_font.render(f"{datas[i][0]}", True, color), (550,data_y + 30*i)) ; screen.blit(table_font.render(f"{datas[i][1]}", True, color), (750,data_y + 30*i))
            
            if 760 < x < 830 and 170 < y <200: # 更改材料
                pg.draw.rect(screen, (233,138,121), [760,170,70,30],0)
                screen.blit(inner_font.render("Change", True, (255,255,255)), (762,175))
                if mouse[0]: 
                    for i in range(len(datas)): sel_data.append(datas[i][0])
                    cocktail_mode = 5 
                    
            else:
                pg.draw.rect(screen, (226,226,226), [760,170,70,30],0)
                screen.blit(inner_font.render("Change", True, (0,0,0)), (762,175))
            
            if 760 < x < 830 and 220 < y <250: # 新增材料
                pg.draw.rect(screen, (233,138,121), [760,220,70,30],0)
                screen.blit(inner_font.render("Add", True, (255,255,255)), (778,225))
                if mouse[0]: 
                    ing_data = data_db.find("SELECT * FROM `ingredients of wine`")
                    cocktail_mode = 7
                    for i in range(len(ing_data)): sel_data.append(ing_data[i][1])
                    
            else:
                pg.draw.rect(screen, (226,226,226), [760,220,70,30],0)
                screen.blit(inner_font.render("Add", True, (0,0,0)), (778,225))
            
            if 180 < x < 250 and 530 < y <560: # 上一頁
                pg.draw.rect(screen, (233,138,121), [180,530,70,30],0)
                screen.blit(inner_font.render("Last", True, (255,255,255)), (195,535))
                if mouse[0]: cocktail_mode = 2
            else:
                pg.draw.rect(screen, (226,226,226), [180,530,70,30],0)
                screen.blit(inner_font.render("Last", True, (0,0,0)), (195,535))
                
        if cocktail_mode == 4:
            try:
                name, english_name,production_method,options = TKhelp.cocktail_form(str(coc_text),datas[a_i][2],datas[a_i][3],coc_table)
                if name != "": data_db.insert(f"UPDATE `cocktail list` SET `Name of Cocktail`='{name}'  WHERE `ID of Cocktail` = '{cocktail_id}'")
                if english_name != "": data_db.insert(f"UPDATE `cocktail list` SET `English Name of Cocktail`='{english_name}'  WHERE `ID of Cocktail` = '{cocktail_id}'")
                if production_method != str(coc_text): data_db.insert(f"UPDATE `cocktail list` SET `Production Method` ='作法： \n{production_method}'  WHERE `ID of Cocktail` = '{cocktail_id}'")
                if True in options: 
                    for i in range(len(options)):
                        if options[i] == True:
                            data_db.insert(f"UPDATE `cocktail list` SET {table_list2[i]} ='1'  WHERE `ID of Cocktail` = '{cocktail_id}'")
                        else: 
                            data_db.insert(f"UPDATE `cocktail list` SET {table_list2[i]} = NUll WHERE `ID of Cocktail` = '{cocktail_id}'")
            except:
                pass
            cocktail_mode = 2
            
        if cocktail_mode == 5: #更改原有內容
            try:
                selection ,used = TKhelp.change_from(sel_data)
                ing_id = data_db.find(f"SELECT `ID of Ingredients` FROM `ingredients of wine` WHERE `Name of Ingredients` = '{selection}'")[0][0]
                if used != "": data_db.insert(f"UPDATE `ingredients of cocktail` SET `Amount of used`='{used}' WHERE `ID of Ingredients` = '{ing_id}' and `ID of Cocktail` = '{cocktail_id}' ")
            except:
                pass
            cocktail_mode = 3
        
        if cocktail_mode == 6:
            screen.blit(background, (0,0))
            pg.draw.rect(screen, (255,255,255), [380,190,280,200],0)
            screen.blit(title2_font.render("是否刪除?", True, (36,45,55)), (457,200))
            if 420 < x < 460 and 300 < y < 340:
                screen.blit(title2_font.render("是", True, (233,138,121)), (420,300))
                
                if mouse[0]: 
                    if del_item:
                        cocktail_mode = 3 ; del_item = 0 
                        data_db.insert(f"DELETE FROM `ingredients of cocktail` WHERE `ID of Ingredients`='{ing_id}' and `ID of Cocktail`='{cocktail_id}'")
                    else:
                        cocktail_mode = 1 ; data_db.insert(f" DELETE FROM `cocktail list` WHERE `ID of Cocktail` = '{cocktail_id}' ") 
                                   
                    #"DELETE FROM `ingredients of cocktail` WHERE `ID of Ingredients`={} `ID of Cocktail`={}"
            else:
                screen.blit(title2_font.render("是", True, (190,190,190)), (420,300))
            
            if 580 < x < 620 and 300 < y < 340:
                screen.blit(title2_font.render("否", True, (233,138,121)), (580,300))
                if mouse[0]:
                    if del_item:
                        cocktail_mode = 3 ; del_item = 0
                    else:
                        cocktail_mode = 2
            else:
                screen.blit(title2_font.render("否", True, (190,190,190)), (580,300))
        
        if cocktail_mode == 7: #增加新的材料
            try:
                aa = []
                data_ID = data_db.find(f"SELECT `ingredients of cocktail`.`ID of Ingredients` FROM `ingredients of cocktail` , `ingredients of wine` WHERE `ingredients of cocktail`.`ID of Ingredients` = `ingredients of wine`.`ID of Ingredients` and `ingredients of cocktail`.`ID of Cocktail` = '{cocktail_id}';")
                for i in range(len(data_ID)): aa.append(data_ID[i][0])
                
                selection ,used = TKhelp.change_from(sel_data)
                ing_id = data_db.find(f"SELECT `ID of Ingredients` FROM `ingredients of wine` WHERE `Name of Ingredients` = '{selection}'")[0][0]
                if ing_id in aa:
                    pass
                else:
                    if used != "": data_db.insert(f"INSERT INTO `ingredients of cocktail`(`ID of Ingredients`, `ID of Cocktail`, `Amount of used`) VALUES ('{ing_id}','{cocktail_id}','{used}')")
                    
            except:
                pass
            cocktail_mode = 3
            
        if cocktail_mode == 8:
            datas = data_db.find(" SELECT * FROM `cocktail list` ")
           
            try:
                new_id = int(datas[len(datas)-1][0][1:])+1
                if new_id < 10: new_id = f'C0{new_id}'
                else: new_id = f'C{new_id}'
                
                opts, name, english_name,production_method,options = TKhelp.cocktail_add()
                T_int = "'1'" ; F_int = 'NUll'
                if name !="": 
                    table_list = []
                    for i in options:
                        if i: table_list.append(T_int)
                        else: table_list.append(F_int)
                    data_db.insert(f"""INSERT INTO `cocktail list`(`ID of Cocktail`, `ID of Liquor`, `Name of Cocktail`, `English Name of Cocktail`, `Production Method`, `Low alcohol concentration`, `Medium alcohol concentration`, `High alcohol concentration`, `Sour`, `Sweet`, `bitter`, `spicy`, `Ice`, `Hot`) VALUES ('{new_id}','{opts}','{name}','{english_name}','作法： \n{production_method}',{table_list[0]},{table_list[1]},{table_list[2]},{table_list[3]},{table_list[4]},{table_list[5]},{table_list[6]},{table_list[7]},{table_list[8]})""")
                row_x = 10 ;
            except:
                pass #資料尚未完全輸入
            cocktail_mode = 1
            
    if mode == 5:
        counter += 1
        screen.blit(inner_font.render("Ingredients", True, (43,192,109)), (10,400))
        screen.blit(show_font.render("Add or delete drink ", True, (178,203,221)), (15,425))
        screen.blit(show_font.render("ingredients", True, (178,203,221)), (15,445))
        if ingredients_mode == 1:
            screen.blit(title_font.render("Ingredients Basic", True, (36,45,55)), (180,65))
            pg.draw.rect(screen, (226,226,226), [180,110,650,30],0)
            datas = data_db.find("SELECT * FROM `ingredients of wine`")
            ing_list = []
            #table desgin
            screen.blit(inner_font.render("ID", True, (0,0,0)), (230,115))
            screen.blit(inner_font.render("Name", True, (0,0,0)), (350,115))
            screen.blit(inner_font.render("Origin", True, (0,0,0)), (580,115))
            
            if first+row_x >= len(datas): row_x = len(datas) - first 
            else: row_x = 10
            s = 0
            for i in range(first,first+row_x):
                if data_x < x and data_y+30*s < y < data_y+30*(s+1) and x <700: 
                    color = (233,138,121)
                    if mouse[0]: 
                        a_i = i; ingredients_mode =2
                        
                else:
                    color = (0,0,0)            
                screen.blit(table_font.render(f"{datas[i][0]}", True, color), (data_x+45,data_y+30*s))
                screen.blit(table_font.render(f"{datas[i][1]}", True, color), (data_x+160,data_y+30*s))
                screen.blit(table_font.render(f"{datas[i][2]}", True, color), (data_x+400,data_y+30*s))
                s += 1
            
            if first > -1 and first+row_x < len(datas):
                if 760 < x < 830 and 530 < y <560 and not_in: # 下一頁
                    pg.draw.rect(screen, (233,138,121), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (255,255,255)), (775,535))
                    if mouse[0] and counter > 12 : 
                        first +=10 ; counter = 0 ;  data_x = 180 ; data_y = 150
                else:
                    pg.draw.rect(screen, (226,226,226), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (0,0,0)), (775,535))
            if first > 0:
                if 180 < x < 250 and 530 < y <560: # 上一頁
                    pg.draw.rect(screen, (233,138,121), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (255,255,255)), (195,535))
                    if mouse[0] and counter > 12 : 
                        first -=10 ; counter = 0 ;  data_x = 180 ; data_y = 150
                else:
                    pg.draw.rect(screen, (226,226,226), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (0,0,0)), (195,535))
        
            if 760 < x < 830 and 170 < y <200: # 新增材料
                pg.draw.rect(screen, (233,138,121), [760,170,70,30],0)
                screen.blit(inner_font.render("Add", True, (255,255,255)), (778,175))
                if mouse[0]: 
                    for i in range(len(datas)): ing_list.append(datas[i][1])
                    new_id = int(datas[len(datas)-1][0][1:])+1
                    ingredients_mode = 5
                
            else:
                pg.draw.rect(screen, (226,226,226), [760,170,70,30],0)
                screen.blit(inner_font.render("Add", True, (0,0,0)), (778,175))
        
        if ingredients_mode == 2:
            data_x = 180 ; data_y = 290
            datas = data_db.find("SELECT * FROM `ingredients of wine`")
            screen.blit(title_font.render("Ingredients Advanced", True, (36,45,55)), (180,65))
            pg.draw.rect(screen, (226,226,226), [180,110,650,30],0)
            screen.blit(title2_font.render(f"{datas[a_i][1]}", True, (0,0,0)), (180,150))
            screen.blit(table_font.render(f"ID : {datas[a_i][0]}", True, (0,0,0)), (180,200))
            screen.blit(table_font.render(f"Origin : {datas[a_i][2]}", True, (0,0,0)), (180,230))
            screen.blit(table_font.render("Website : ", True, (0,0,0)), (180,260))
            s = 0
            for i in range(len(datas[a_i][3])): 
                if s > 35: data_x = 180 ; data_y += 30 ; s = 0
                screen.blit(table_font.render(f"{datas[a_i][3][i]}", True, (0,0,0)), (data_x+18*s,data_y))
                s += 1
            
            if 760 < x < 830 and 220 < y <250: # 修改內容
                pg.draw.rect(screen, (233,138,121), [760,220,70,30],0)
                screen.blit(inner_font.render("Change", True, (255,255,255)), (762,225))
                if mouse[0]: ingredients_mode = 3 ; ing_id = datas[a_i][0] 
            else:
                pg.draw.rect(screen, (226,226,226), [760,220,70,30],0)
                screen.blit(inner_font.render("Change", True, (0,0,0)), (762,225))
                
            if 760 < x < 830 and 170 < y <200: # 刪除材料
                pg.draw.rect(screen, (233,138,121), [760,170,70,30],0)
                screen.blit(inner_font.render("Delete", True, (255,255,255)), (765,175))
                if mouse[0]: 
                    ingredients_mode = 4 ; ing_id = datas[a_i][0]
            else:
                pg.draw.rect(screen, (226,226,226), [760,170,70,30],0)
                screen.blit(inner_font.render("Delete", True, (0,0,0)), (765,175))
        
        if ingredients_mode == 3:
            try:
                name, origin, website = TKhelp.ing_form(datas[a_i][1])
                if name !="": data_db.insert(f"UPDATE `ingredients of wine` SET `Name of Ingredients`='{name}' WHERE `ID of Ingredients` = '{ing_id}' ")
                if origin != "": data_db.insert(f"UPDATE `ingredients of wine` SET `Origin`='{origin}' WHERE `ID of Ingredients` = '{ing_id}' ")
                if website != "": data_db.insert(f"UPDATE `ingredients of wine` SET `Website`='{website}' WHERE `ID of Ingredients` = '{ing_id}' ")
            except:
                pass
            ingredients_mode = 2
            
        if ingredients_mode == 4:
            
            screen.blit(background, (0,0))
            pg.draw.rect(screen, (255,255,255), [380,190,280,200],0)
            screen.blit(title2_font.render("是否刪除該材料?", True, (36,45,55)), (410,200))
            if 420 < x < 460 and 300 < y < 340:
                screen.blit(title2_font.render("是", True, (233,138,121)), (420,300))
                if mouse[0]: 
                    data_db.insert(f" DELETE FROM `ingredients of wine` WHERE `ID of Ingredients` = '{ing_id}'")            
                    data_db.insert(f"DELETE FROM ingredients of cocktail WHERE `ingredients of cocktail`.`ID of Ingredients` = '{ing_id}'")
                    ingredients_mode = 1
            else:
                screen.blit(title2_font.render("是", True, (190,190,190)), (420,300))
            
            if 580 < x < 620 and 300 < y < 340:
                screen.blit(title2_font.render("否", True, (233,138,121)), (580,300))
                if mouse[0]: ingredients_mode = 2
            else:
                screen.blit(title2_font.render("否", True, (190,190,190)), (580,300))
    
        if ingredients_mode == 5:
           # print(datas[a_i][1])
            try:
                name, origin, website = TKhelp.ing_form()
                if name != "" and name not in ing_list: data_db.insert(f"INSERT INTO `ingredients of wine`(`ID of Ingredients`, `Name of Ingredients`, `Origin`, `Website`) VALUES ('{new_id}','{name}','{origin}','{website}')")
            except:
                pass
            ingredients_mode = 1
    
    if mode == 6:
        counter += 1
        screen.blit(inner_font.render("Comment", True, (43,192,109)), (10,480))
        screen.blit(show_font.render("Add or delete ", True, (178,203,221)), (15,505))
        screen.blit(show_font.render("negative comments", True, (178,203,221)), (15,525))
        screen.blit(pg.image.load("./image/back.png"),(170,52))
        
        if 0 in fish_type:
            for i in range(6):
                if fish_type[i] == 0: 
                    if fish_move[i] == 1:
                        sur = pg.transform.scale(pg.image.load(f'./image/tile{i+1}.png'), (64,64)) ; sur_2 = pg.transform.flip(sur, True,False)
                        screen.blit(sur_2,(fish_x[i],fish_y[i]))
                    else:
                       screen.blit(pg.transform.scale(pg.image.load(f'./image/tile{i+1}.png'), (64,64)), (fish_x[i],fish_y[i]))
        
        if fish_mode == 1:
            if 172 < x < 192 and 60 < y < 130:
                pg.draw.rect(screen, (36,45,55), [172,60,20,70],0)
                pg.draw.rect(screen, (255,255,255), [179,70,5,50],0) 
                if counter > 20:
                    if mouse[0]:
                        fish_mode = 2 ; counter = 0
            else:
                pg.draw.rect(screen, (255,255,255), [172,60,20,70],0)
                pg.draw.rect(screen, (36,45,55), [179,70,5,50],0) 
                    
                   
        if fish_mode == 2:
            pg.draw.rect(screen, (255,255,255), [172,60,500,70],0)
            pg.draw.rect(screen, (36,45,55), [179,70,5,50],0) 
            for i in range(1,7):
                if fish_type[i-1]:
                    if 130+i*75 < x < 130+(i+1)*75 and 60 < y < 130:
                        pg.draw.rect(screen, (178,203,221), [130+i*75,63,64,64],0)
                        if mouse[0] and counter >10 :
                            fish_mode = 3 ; a_i = i
                    screen.blit(pg.transform.scale(pg.image.load(f'./image/tile{i}.png'), (64,64)), (130+i*75,60))
                else:
                    if 130+i*75 < x < 130+(i+1)*75 and 60 < y < 130:
                        pg.draw.rect(screen, (178,203,221), [130+i*75,63,64,64],0)
                        if mouse[0]:
                            fish_type[i-1] = 1 ; counter = 0
            if counter > 20:
                if 172 < x < 192 and 60 < y < 130:              
                    if mouse[0]:
                        fish_mode = 1 ; counter = 0
                        
            
        if fish_mode == 3:
            if mouse[0]:
                screen.blit(pg.transform.scale(pg.image.load(f'./image/tile{a_i}.png'), (64,64)), (x-30,y-30))
            else:
                fish_type[a_i-1] = 0 ; fish_x[a_i-1] = x-30 ; fish_y[a_i-1] = y-30
                fish_mode = 1
             
        
        if 0 in fish_type:
            for i in range(6):
                if fish_type[i] == 0:
                    if fish_x[i] <= 170:
                        fish_move[i] = 1
                    elif fish_x[i] >= 832:
                        fish_move[i] = -1
                        
                    if fish_y[i] <= 52:
                        fish_ran[i] = random.randint(1, 3)
                    elif fish_y[i] >= 532:
                        fish_ran[i] = random.randint(-3, -1)
                    
                    if fish_move[i] == -1:
                        fish_x[i] -= 3
                        fish_y[i] += fish_ran[i]
                    else:
                        fish_x[i] += 3
                        fish_y[i] += fish_ran[i]
                        
    if mode == 7:
        counter += 1
        screen.blit(inner_font.render("Comment", True, (43,192,109)), (10,480))
        screen.blit(show_font.render("Add or delete ", True, (178,203,221)), (15,505))
        screen.blit(show_font.render("negative comments", True, (178,203,221)), (15,525))
        if comment_mode == 1:
            data_x = 200 ; data_y = 150 ; counter +=1
            screen.blit(title_font.render("Comment" ,True, (36,45,55)), (180,65))
            datas = data_db.find(" SELECT * FROM `cocktail of message` ")
            pg.draw.rect(screen, (226,226,226), [180,110,700,30],0)
        
            screen.blit(inner_font.render("Cocktial", True, (0,0,0)), (200,115))
            screen.blit(inner_font.render("User ID", True, (0,0,0)), (350,115))
            screen.blit(inner_font.render("Message", True, (0,0,0)), (550,115))
            screen.blit(inner_font.render("Level", True, (0,0,0)), (800,115))
            
            if first+row_x >= len(datas): row_x = len(datas) - first 
            else: row_x = 10
            s = 0
            
            if first_run:
                screen.blit(background, (0,0))
                screen.blit(title2_font.render("Loading...", True, (36,45,55)), (410,300))
                pg.display.update()
                for i in range(first,first+row_x):
                    ans = sentiment_analysis.mood_analy(f"{datas[i][2]}")
                    ana_per.append(ans[0]) ; ana_msg.append(ans[1]) 
                    page[read_page] = 1
                    
            first_run = 0
            
            for i in range(first,first+row_x): 
                if data_y + 30*s < y < data_y + 30*(s+1) and 200 < x < 880 and counter > 12: 
                    color = (233,138,121)
                    if mouse[0]:  comment_mode = 2 ; a_i = i ; counter = 0
                else: color = (0,0,0)
                
                coc_name = data_db.find(f"SELECT `Name of Cocktail` FROM `cocktail list` WHERE `ID of Cocktail` ='{datas[i][0]}';")[0][0]
                
                screen.blit(table_font.render(f"{coc_name}", True, color), (data_x,data_y + 30*s)) 
                screen.blit(table_font.render(f"{datas[i][1]}", True, color), (370,data_y + 30*s))
                if len(datas[i][2]) >13:
                    screen.blit(table_font.render(f"{datas[i][2][:13]}...", True, color), (500,data_y + 30*s))
                else:
                    screen.blit(table_font.render(f"{datas[i][2]}", True, color), (500,data_y + 30*s))
                screen.blit(table_font.render(f"{ana_msg[i]}", True, color), (800,data_y + 30*s))
                s += 1   
            
            if first > -1 and first+row_x < len(datas):
                if 760 < x < 830 and 530 < y <560 and not_in: # 下一頁
                    pg.draw.rect(screen, (233,138,121), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (255,255,255)), (775,535))
                    if mouse[0] and counter > 12 : 
                        first +=10 ; counter = 0 ;  data_x = 160 ; data_y = 150  ; read_page += 1
                        if not page[read_page]: first_run=1
                else:
                    pg.draw.rect(screen, (226,226,226), [760,530,70,30],0)
                    screen.blit(inner_font.render("Next", True, (0,0,0)), (775,535))
            if first > 0:
                if 180 < x < 250 and 530 < y <560: # 上一頁
                    pg.draw.rect(screen, (233,138,121), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (255,255,255)), (195,535))
                    if mouse[0] and counter > 12 : 
                        first -=10 ; counter = 0 ;  data_x = 160 ; data_y = 150  ; read_page -= 1
                else:
                    pg.draw.rect(screen, (226,226,226), [180,530,70,30],0)
                    screen.blit(inner_font.render("Last", True, (0,0,0)), (195,535))
        
        if comment_mode == 2:
            data_x = 200 ; data_y = 240
            color = (0,0,0) ; counter +=1
            screen.blit(title_font.render("Comment Detail" ,True, (36,45,55)), (180,65)) 
            coc_name = data_db.find(f"SELECT `Name of Cocktail` FROM `cocktail list` WHERE `ID of Cocktail` ='{datas[a_i][0]}';")[0][0]
            user_name = data_db.find(f"SELECT `User_name` FROM `account` WHERE `ID of Account` = '{datas[a_i][1]}';")[0][0]
            screen.blit(table_font.render(f"Cocktail Name: {coc_name}", True, color), (180,150)) 
            screen.blit(table_font.render(f"User Name: {user_name}", True, color), (180,180))
            screen.blit(table_font.render("User comment:", True, color), (180,210))
            
            for i in range(len(datas[a_i][2])):
                screen.blit(table_font.render(f"{datas[a_i][2][i]}", True, color), (data_x,data_y))
                data_x += 20
                if not(i % 20) and i != 0: 
                    data_x = 200 ; data_y += 30
            
            screen.blit(table_font.render(f"Level: {ana_msg[a_i]}", True, color), (180,470))
            per = int(ana_per[a_i]*100) #正負面%
            pg.draw.rect(screen, (226,226,226), [200,510,600,20],0)
            if 2*counter < 6*per:
                pg.draw.rect(screen, (233,138,121), [200,510,2*counter,20],0)
            else:
                pg.draw.rect(screen, (233,138,121), [200,510,6*per,20],0)
            
            screen.blit(table_font.render(f"{per} %", True, (255,255,255)), (205,510))
            screen.blit(table_font.render(f"{100 - per} %", True, (0,0,0)), (765,510))
            
              
            if 810 < x < 880 and 170 < y <200: # 新增材料
                pg.draw.rect(screen, (233,138,121), [810,170,70,30],0)
                screen.blit(inner_font.render("Delete", True, (255,255,255)), (817,175))
                if mouse[0]: 
                    comment_mode = 3
            else:
                pg.draw.rect(screen, (226,226,226), [810,170,70,30],0)
                screen.blit(inner_font.render("Delete", True, (0,0,0)), (817,175))
                
        if comment_mode == 3:
            screen.blit(background, (0,0))
            pg.draw.rect(screen, (255,255,255), [380,190,280,200],0)
            screen.blit(title2_font.render("是否刪除該言論?", True, (36,45,55)), (410,200))
            if 420 < x < 460 and 300 < y < 340:
                screen.blit(title2_font.render("是", True, (233,138,121)), (420,300))
                if mouse[0]: 
                    data_db.insert(f"DELETE FROM `cocktail of message` WHERE `Message` = '{datas[a_i][2]}' and `ID of Cocktail` = '{datas[a_i][0]}' and `ID of Account` = '{datas[a_i][1]}'")
                    comment_mode = 1 ; counter = 0
                    
            else:
                screen.blit(title2_font.render("是", True, (190,190,190)), (420,300))
            
            if 580 < x < 620 and 300 < y < 340:
                screen.blit(title2_font.render("否", True, (233,138,121)), (580,300))
                if mouse[0]: comment_mode = 2
            else:
                screen.blit(title2_font.render("否", True, (190,190,190)), (580,300))
    pg.display.update()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
pg.quit()