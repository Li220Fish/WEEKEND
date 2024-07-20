import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def login_from():
    def submit():
        global log
        name = name_entry.get()
        password = pass_entry.get()
        
        if name == 'root':
            if password == '123':
                log = '    Correct'
            else:
                log = 'Password Error'
        else:
            log = '  Account Error'
        
        root.destroy()
        
    root = tk.Tk()
    root.title("Login")

    name_label = tk.Label(root, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    pass_label = tk.Label(root, text="Password:")
    pass_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    pass_entry = tk.Entry(root)
    pass_entry.grid(row=1, column=1, padx=5, pady=5)
    
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=3, column=0, padx=10, pady=10)
    
    root.mainloop()
    return log

def wine_form(i_name,i_english,i_alcohol,i_origin,i_capacity,i_price):
    def submit():
        global name, english_name, alcohol, origin, capacity, price
        name = name_entry.get()
        english_name = english_name_entry.get()
        alcohol = alcohol_entry.get()
        origin = combobox.get()
        capacity = capacity_entry.get()
        price = price_entry.get()
        root.destroy()
 
    root = tk.Tk()
    root.title("Input Form")

    # 调整窗口大小
    root.geometry("300x250")
    
    global_countries = [
    "台灣","美國", "加拿大", "墨西哥", "巴西", "阿根廷", "英國",
    "德國", "法國", "義大利", "西班牙", "俄羅斯", "中國", "印度", "日本",
    "韓國", "澳大利亞", "紐西蘭", "南非", "埃及", "尼日利亞",
    "肯尼亞", "沙烏地阿拉伯", "土耳其", "伊朗", "巴基斯坦", "孟加拉",
    "印尼", "馬來西亞", "新加坡", "泰國", "越南", "菲律賓", "緬甸", "斯里蘭卡",
    "尼泊爾", "不丹", "馬爾地夫", "阿富汗", "烏茲別克", "哈薩克", "土庫曼", 
    "吉爾吉斯", "塔吉克", "喬治亞", "亞美尼亞", "亞塞拜然", "烏克蘭", "白俄羅斯",
    "波蘭", "捷克", "斯洛伐克", "匈牙利", "羅馬尼亞", "保加利亞", "希臘",
    "瑞典", "挪威", "丹麥", "芬蘭", "冰島", "愛爾蘭", "葡萄牙", "荷蘭",
    "比利時", "瑞士", "奧地利", "盧森堡", "列支敦士登", "摩納哥", "聖馬利諾",
    "梵蒂岡", "馬耳他", "賽普勒斯", "以色列", "約旦", "黎巴嫩", "敘利亞", "伊拉克", "也門",
    "阿曼", "阿聯酋", "卡塔爾", "巴林", "科威特", "摩洛哥", "阿爾及利亞", "突尼斯",
    "利比亞", "蘇丹", "衣索比亞", "索馬里", "烏干達", "盧旺達", "蒲隆地", "坦尚尼亞", "尚比亞",
    "辛巴威", "波札那", "納米比亞", "安哥拉", "莫三比克", "馬達加斯加", "塞席爾", "模里西斯",
    "葛摩", "南蘇丹", "中非共和國", "查德", "尼日", "馬利", "茅利塔尼亞",
    "塞內加爾", "甘比亞", "幾內亞", "幾內亞比紹", "獅子山", "賴比瑞亞", "象牙海岸",
    "迦納", "多哥", "貝南", "布吉納法索", "維德角", "厄利垂亞", "吉布地", "索馬利蘭",
    "西撒哈拉", "巴勒斯坦"]
    # 创建标签和文本框
    tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(root)
    name_entry.insert(0, i_name)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="English Name:").grid(row=1, column=0, padx=10, pady=5)
    english_name_entry = tk.Entry(root)
    english_name_entry.insert(0, i_english)
    english_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Alcohol:").grid(row=2, column=0, padx=10, pady=5)
    alcohol_entry = tk.Entry(root)
    alcohol_entry.insert(0, i_alcohol)
    alcohol_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Origin:").grid(row=3, column=0, padx=10, pady=5)
    selected_option = tk.StringVar(root)
    #selected_option.set(global_countries[0])
    combobox = ttk.Combobox(root, textvariable=selected_option, values=global_countries)
    combobox.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(root, text="Capacity(ml):").grid(row=4, column=0, padx=10, pady=5)
    capacity_entry = tk.Entry(root)
    capacity_entry.insert(0, i_capacity)
    capacity_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(root, text="Price(TWD):").grid(row=5, column=0, padx=10, pady=5)
    price_entry = tk.Entry(root)
    price_entry.insert(0, i_price)
    price_entry.grid(row=5, column=1, padx=10, pady=5)

    # 创建提交按钮
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)
 
    root.mainloop()
    return name, english_name, alcohol, origin, capacity, price

def wine_add():
    def submit():
        global  opts, name, english_name, alcohol, origin, capacity, price
        options = combobox.get()
        name = name_entry.get()
        english_name = english_name_entry.get()
        alcohol = alcohol_entry.get()
        origin = combobox.get()
        capacity = capacity_entry.get()
        price = price_entry.get()
        s = 1
        for i in ['Vodka', 'Rum', 'Brandy', 'Liqeur','Gin','Tequila','Wiskey']:
            if options == i: opts = f'A0{s}' ; break
            s += 1
        root.destroy()
        
    root = tk.Tk()
    root.title("Input Form")

    # 调整窗口大小
    #root.geometry("300x250")
    global_countries = [
    "台灣","美國", "加拿大", "墨西哥", "巴西", "阿根廷", "英國",
    "德國", "法國", "義大利", "西班牙", "俄羅斯", "中國", "印度", "日本",
    "韓國", "澳大利亞", "紐西蘭", "南非", "埃及", "尼日利亞",
    "肯尼亞", "沙烏地阿拉伯", "土耳其", "伊朗", "巴基斯坦", "孟加拉",
    "印尼", "馬來西亞", "新加坡", "泰國", "越南", "菲律賓", "緬甸", "斯里蘭卡",
    "尼泊爾", "不丹", "馬爾地夫", "阿富汗", "烏茲別克", "哈薩克", "土庫曼", 
    "吉爾吉斯", "塔吉克", "喬治亞", "亞美尼亞", "亞塞拜然", "烏克蘭", "白俄羅斯",
    "波蘭", "捷克", "斯洛伐克", "匈牙利", "羅馬尼亞", "保加利亞", "希臘",
    "瑞典", "挪威", "丹麥", "芬蘭", "冰島", "愛爾蘭", "葡萄牙", "荷蘭",
    "比利時", "瑞士", "奧地利", "盧森堡", "列支敦士登", "摩納哥", "聖馬利諾",
    "梵蒂岡", "馬耳他", "賽普勒斯", "以色列", "約旦", "黎巴嫩", "敘利亞", "伊拉克", "也門",
    "阿曼", "阿聯酋", "卡塔爾", "巴林", "科威特", "摩洛哥", "阿爾及利亞", "突尼斯",
    "利比亞", "蘇丹", "衣索比亞", "索馬里", "烏干達", "盧旺達", "蒲隆地", "坦尚尼亞", "尚比亞",
    "辛巴威", "波札那", "納米比亞", "安哥拉", "莫三比克", "馬達加斯加", "塞席爾", "模里西斯",
    "葛摩", "南蘇丹", "中非共和國", "查德", "尼日", "馬利", "茅利塔尼亞",
    "塞內加爾", "甘比亞", "幾內亞", "幾內亞比紹", "獅子山", "賴比瑞亞", "象牙海岸",
    "迦納", "多哥", "貝南", "布吉納法索", "維德角", "厄利垂亞", "吉布地", "索馬利蘭",
    "西撒哈拉", "巴勒斯坦"]
    
    options = ['Vodka', 'Rum', 'Brandy', 'Liqeur','Gin','Tequila','Wiskey']
    selected_option = tk.StringVar(root)
    selected_option.set(options[0])  # set the default option
    tk.Label(root, text="Liquor:").grid(row=0, column=0, padx=10, pady=5)
    combobox = ttk.Combobox(root, textvariable=selected_option, values=options)
    combobox.grid(row=0, column=1, padx=10, pady=10)

    # 创建标签和文本框
    tk.Label(root, text="Name:").grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="English Name:").grid(row=2, column=0, padx=10, pady=5)
    english_name_entry = tk.Entry(root)
    english_name_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Alcohol:").grid(row=3, column=0, padx=10, pady=5)
    alcohol_entry = tk.Entry(root)
    alcohol_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Origin:").grid(row=4, column=0, padx=10, pady=5)
    selected_option = tk.StringVar(root)
    #selected_option.set(global_countries[0])
    combobox = ttk.Combobox(root, textvariable=selected_option, values=global_countries)
    combobox.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(root, text="Capacity(ml):").grid(row=5, column=0, padx=10, pady=5)
    capacity_entry = tk.Entry(root)
    capacity_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(root, text="Price(TWD):").grid(row=6, column=0, padx=10, pady=5)
    price_entry = tk.Entry(root)
    price_entry.grid(row=6, column=1, padx=10, pady=5)

    # 创建提交按钮
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=7, column=0, columnspan=2, pady=10)
 
    root.mainloop()
    return opts, name, english_name, alcohol, origin, capacity, price

def cocktail_form(text,i_name,i_english,coc_table):
    def submit():
        global name, english_name,production_method,options
        name = name_entry.get()
        english_name = english_name_entry.get()
        production_method = production_method_entry.get()
        options = [low_var.get(), med_var.get(), high_var.get(), sour_var.get(), sweet_var.get(), bitter_var.get(), spicy_var.get(), ice_var.get(), hot_var.get()]
        root.destroy()
    root = tk.Tk()
    root.title("Input Form")
    
    # Name
    name_label = tk.Label(root, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_entry = tk.Entry(root)
    name_entry.insert(0,i_name)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    # English Name
    english_name_label = tk.Label(root, text="English Name:")
    english_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    english_name_entry = tk.Entry(root)
    english_name_entry.insert(0,i_english)
    english_name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    # Production Method
    production_method_label = tk.Label(root, text="Production Method:")
    production_method_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    production_method_entry = tk.Entry(root)
    production_method_entry.grid(row=2, column=1, padx=5, pady=5,ipady=50)
    production_method_entry.insert(0, f"{text}")
    # Options
    options_frame = tk.LabelFrame(root, text="Options")
    options_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")
    
    low_var = tk.BooleanVar()
    
    low_checkbox = tk.Checkbutton(options_frame, text="Low", variable=low_var)
    if str(coc_table[0]) == "1":
        low_checkbox.toggle()
    low_checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    med_var = tk.BooleanVar()
    med_checkbox = tk.Checkbutton(options_frame, text="Med", variable=med_var)
    if str(coc_table[1]) == "1":
           med_checkbox.toggle()
    med_checkbox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    high_var = tk.BooleanVar()
    high_checkbox = tk.Checkbutton(options_frame, text="High", variable=high_var)
    if str(coc_table[2]) == "1":
        high_checkbox.toggle()
    high_checkbox.grid(row=0, column=2, padx=5, pady=5, sticky="w")
    
    sour_var = tk.BooleanVar()
    sour_checkbox = tk.Checkbutton(options_frame, text="Sour", variable=sour_var)
    if str(coc_table[3]) == "1":
        sour_checkbox.toggle()
    sour_checkbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    
    sweet_var = tk.BooleanVar()
    sweet_checkbox = tk.Checkbutton(options_frame, text="Sweet", variable=sweet_var)
    if str(coc_table[4]) == "1":
        sweet_checkbox.toggle()
    sweet_checkbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    bitter_var = tk.BooleanVar()
    bitter_checkbox = tk.Checkbutton(options_frame, text="Bitter", variable=bitter_var)
    if str(coc_table[5]) == "1":
        bitter_checkbox.toggle()
    bitter_checkbox.grid(row=1, column=2, padx=5, pady=5, sticky="w")
    
    spicy_var = tk.BooleanVar()
    spicy_checkbox = tk.Checkbutton(options_frame, text="Spicy", variable=spicy_var)
    if str(coc_table[6]) == "1":
        spicy_checkbox.toggle()
    spicy_checkbox.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    
    ice_var = tk.BooleanVar()
    ice_checkbox = tk.Checkbutton(options_frame, text="Ice", variable=ice_var)
    if str(coc_table[7]) == "1":
        ice_checkbox.toggle()
    ice_checkbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    hot_var = tk.BooleanVar()
    hot_checkbox = tk.Checkbutton(options_frame, text="Hot", variable=hot_var)
    if str(coc_table[8]) == "1":
        hot_checkbox.toggle()
    hot_checkbox.grid(row=2, column=2, padx=5, pady=5, sticky="w")
    
    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    root.mainloop()
    return name, english_name,production_method,options

def cocktail_add():
    def submit():
        global opts ,name, english_name,production_method,options
        opts_i = combobox.get()
        name = name_entry.get()
        english_name = english_name_entry.get()
        production_method = production_method_entry.get()
        options = [low_var.get(), med_var.get(), high_var.get(), sour_var.get(), sweet_var.get(), bitter_var.get(), spicy_var.get(), ice_var.get(), hot_var.get()]
        s = 1
        for i in ['Vodka', 'Rum', 'Brandy', 'Liqeur','Gin','Tequila','Wiskey']:
            if opts_i == i: opts = f'A0{s}' ; break
            s += 1
        root.destroy()
    root = tk.Tk()
    root.title("Input Form")
    
    options_label = tk.Label(root, text="Wine:")
    options_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    opt = ['Vodka', 'Rum', 'Brandy', 'Liqeur','Gin','Tequila','Wiskey']
    selected_option = tk.StringVar(root)
    selected_option.set(opt[0])
    
    combobox = ttk.Combobox(root, textvariable=selected_option, values=opt)
    combobox.grid(row=0, column=1, padx=10, pady=10)
    
    # Name
    name_label = tk.Label(root, text="Name:")
    name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    # English Name
    english_name_label = tk.Label(root, text="English Name:")
    english_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    english_name_entry = tk.Entry(root)
    english_name_entry.grid(row=2, column=1, padx=5, pady=5)
    
    # Production Method
    production_method_label = tk.Label(root, text="Production Method:")
    production_method_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    production_method_entry = tk.Entry(root)
    production_method_entry.grid(row=3, column=1, padx=5, pady=5,ipady=50)
    # Options
    options_frame = tk.LabelFrame(root, text="Options")
    options_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")
    
    low_var = tk.BooleanVar()
    low_checkbox = tk.Checkbutton(options_frame, text="Low", variable=low_var)
    low_checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    med_var = tk.BooleanVar()
    med_checkbox = tk.Checkbutton(options_frame, text="Med", variable=med_var)
    med_checkbox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    high_var = tk.BooleanVar()
    high_checkbox = tk.Checkbutton(options_frame, text="High", variable=high_var)
    high_checkbox.grid(row=0, column=2, padx=5, pady=5, sticky="w")
    
    sour_var = tk.BooleanVar()
    sour_checkbox = tk.Checkbutton(options_frame, text="Sour", variable=sour_var)
    sour_checkbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    
    sweet_var = tk.BooleanVar()
    sweet_checkbox = tk.Checkbutton(options_frame, text="Sweet", variable=sweet_var)
    sweet_checkbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    bitter_var = tk.BooleanVar()
    bitter_checkbox = tk.Checkbutton(options_frame, text="Bitter", variable=bitter_var)
    bitter_checkbox.grid(row=1, column=2, padx=5, pady=5, sticky="w")
    
    spicy_var = tk.BooleanVar()
    spicy_checkbox = tk.Checkbutton(options_frame, text="Spicy", variable=spicy_var)
    spicy_checkbox.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    
    ice_var = tk.BooleanVar()
    ice_checkbox = tk.Checkbutton(options_frame, text="Ice", variable=ice_var)
    ice_checkbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    hot_var = tk.BooleanVar()
    hot_checkbox = tk.Checkbutton(options_frame, text="Hot", variable=hot_var)
    hot_checkbox.grid(row=2, column=2, padx=5, pady=5, sticky="w")
    
    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)
    
    root.mainloop()
    return opts, name, english_name,production_method,options

def change_from(opt):
    def submit():
        global selection , entry
        selection = combobox.get()
        entry = used_entry.get()
        
        root.destroy()
        
    root = tk.Tk()
    root.title("Change Form")

    options = opt
    selected_option = tk.StringVar(root)
    selected_option.set(options[0])  # set the default option
    
    combobox = ttk.Combobox(root, textvariable=selected_option, values=options)
    combobox.grid(row=0, column=0, padx=10, pady=10)

    used_label = tk.Label(root, text="Amount of used:")
    used_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    used_entry = tk.Entry(root)
    used_entry.grid(row=2, column=0, padx=5, pady=5)
    
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=3, column=0, padx=10, pady=10)
    
    root.mainloop()
    return selection ,entry

def ing_form(i_name):
    def submit():
        global name, origin,website
        name = name_entry.get()
        origin = combobox.get()
        website = website_entry.get()
        root.destroy()
 
    root = tk.Tk()
    root.title("Input Form")

    # 调整窗口大小
    #root.geometry("300x250")
    global_countries = [
    "台灣","美國", "加拿大", "墨西哥", "巴西", "阿根廷", "英國",
    "德國", "法國", "義大利", "西班牙", "俄羅斯", "中國", "印度", "日本",
    "韓國", "澳大利亞", "紐西蘭", "南非", "埃及", "尼日利亞",
    "肯尼亞", "沙烏地阿拉伯", "土耳其", "伊朗", "巴基斯坦", "孟加拉",
    "印尼", "馬來西亞", "新加坡", "泰國", "越南", "菲律賓", "緬甸", "斯里蘭卡",
    "尼泊爾", "不丹", "馬爾地夫", "阿富汗", "烏茲別克", "哈薩克", "土庫曼", 
    "吉爾吉斯", "塔吉克", "喬治亞", "亞美尼亞", "亞塞拜然", "烏克蘭", "白俄羅斯",
    "波蘭", "捷克", "斯洛伐克", "匈牙利", "羅馬尼亞", "保加利亞", "希臘",
    "瑞典", "挪威", "丹麥", "芬蘭", "冰島", "愛爾蘭", "葡萄牙", "荷蘭",
    "比利時", "瑞士", "奧地利", "盧森堡", "列支敦士登", "摩納哥", "聖馬利諾",
    "梵蒂岡", "馬耳他", "賽普勒斯", "以色列", "約旦", "黎巴嫩", "敘利亞", "伊拉克", "也門",
    "阿曼", "阿聯酋", "卡塔爾", "巴林", "科威特", "摩洛哥", "阿爾及利亞", "突尼斯",
    "利比亞", "蘇丹", "衣索比亞", "索馬里", "烏干達", "盧旺達", "蒲隆地", "坦尚尼亞", "尚比亞",
    "辛巴威", "波札那", "納米比亞", "安哥拉", "莫三比克", "馬達加斯加", "塞席爾", "模里西斯",
    "葛摩", "南蘇丹", "中非共和國", "查德", "尼日", "馬利", "茅利塔尼亞",
    "塞內加爾", "甘比亞", "幾內亞", "幾內亞比紹", "獅子山", "賴比瑞亞", "象牙海岸",
    "迦納", "多哥", "貝南", "布吉納法索", "維德角", "厄利垂亞", "吉布地", "索馬利蘭",
    "西撒哈拉", "巴勒斯坦"]
    # 创建标签和文本框
    tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(root)
    name_entry.insert(0, i_name)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Origin:").grid(row=1, column=0, padx=10, pady=5)
    
    selected_option = tk.StringVar(root)
    #selected_option.set(global_countries[0])
    combobox = ttk.Combobox(root, textvariable=selected_option, values=global_countries)
    combobox.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Label(root, text="Website:").grid(row=2, column=0, padx=10, pady=5)
    website_entry = tk.Entry(root)
    website_entry.grid(row=2, column=1, padx=10, pady=5)


    # 创建提交按钮
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)
 
    root.mainloop()
    return name, origin, website

#print(cocktail_add()[4])
#print(add_from(['apple', 'var', 'pen', 'car']))
#ing_form()
#print(cocktail_form('1','1','1',))
#print(cocktail_form("56456"))