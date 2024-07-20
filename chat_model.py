import numpy as np
from tensorflow.keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras import layers
import tensorflow
import jieba
import csv
import random
import re
from SQL import DataBase

data_db = DataBase()

def read_files():
    path = 'cocktailtest.csv'
    
    all_texts = []
    all_labels = []
    
    with open(path, newline='', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            label = int(row[0])  
            text = row[1]         
            all_texts.append(text)
            all_labels.append(label)

    return all_texts, all_labels

def preprocess_data():
    train, label = read_files()

    # 取得停用詞
    stopWords = []
    with open('wordstop.txt', 'r', encoding='utf8') as f:
        stopWords = f.read().split('\n')
        stopWords.append('\n')

    z_shuffle = list(zip(train, label))
    random.shuffle(z_shuffle)
    x_train, y_label = zip(*z_shuffle)

    from tensorflow.keras.utils import to_categorical
    num_classes = 8  # 类别数
    y_label = to_categorical(y_label, num_classes=num_classes)

    return x_train, y_label, stopWords

def tokenize_and_pad(x_train, stopWords):
    sentence = []
    for content in x_train:
        _sentence = list(jieba.cut(content, cut_all=True))
        sentence.append(_sentence)
            
    remainderWords2 = []
    for content in sentence:
        remainderWords2.append(list(filter(lambda a: a not in stopWords, content)))

    token = Tokenizer(num_words=3000)
    token.fit_on_texts(remainderWords2)
    x_train_seq = token.texts_to_sequences(remainderWords2)
    x_train_padded = sequence.pad_sequences(x_train_seq, maxlen=100)
    
    return x_train_padded, token  # Return token as well

def test_model(model, tokenizer, stopWords, input_text):
    input_seq = tokenizer.texts_to_sequences([list(jieba.cut(input_text, cut_all=True))])
    input_padded = sequence.pad_sequences(input_seq, maxlen=100)
    prediction = model.predict(input_padded)
    predicted_class = np.argmax(prediction)
    return predicted_class

reload_model = tensorflow.keras.models.load_model('.acras_model.keras')
x_train, y_label, stopWords = preprocess_data()
x_train_processed, token = tokenize_and_pad(x_train, stopWords)  # 预处理训练数据

def validate_input(input_text):
    if not input_text.strip():
        #print("請再重新輸入")
        return False

    if re.match("^[a-zA-Z0-9 ,._-]+$", input_text):
        #print("請再重新輸入。")
        return False

    if len(input_text) > 100:
        #print("輸入過長請重新輸入")
        return False

    return True    

def is_relevant(input_text):
    common_keywords = ["#1","#3","#2","甜", "苦", "酸", "辣", "冰", "澀","蜜", "冷","霜", "熱", "酒精", "濃度", "調酒", "酒量","含量", "酒","做", "中", "高", "低", "好","材料", "過敏", "作法", "做法", "微醺", "烈", "常溫", "室溫", "燙","推薦", "寒冷", "寒", "可以", "無", "不","推荐","醉","最多","讚"]
    input_words = input_text.lower().split()
    #print(input_words)
    for word in input_words:
        if any(keyword in word for keyword in common_keywords):
            return True
    return False 
   

def chatbot(input_text):
        try:
            if not validate_input(input_text[2:]):
                return {"Message":"請重新輸入" ,"Special":"#0" }

            if not is_relevant(input_text[2:]):
                return {"Message":"請重新輸入" ,"Special":"#0" }

            if "過敏" in input_text[2:]:
                return {"Message":"請輸入要排除的材料（如果有多個材料請用逗號分開）：" ,"Special":"#1" }
            if "#1" in input_text:
                exclude_ingredients = input_text[4:]#input("请输入要排除的材料（如果有多个材料请用逗号分隔）：").split(",")
                all_found_records = []

                for ingredient in exclude_ingredients:
                    sql_query = """
                    SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                    FROM `cocktail list`
                    WHERE NOT EXISTS (
                        SELECT *
                        FROM `ingredients of wine`, `ingredients of cocktail`
                        WHERE `ingredients of wine`.`ID of Ingredients` = `ingredients of cocktail`.`ID of Ingredients`
                        AND `cocktail list`.`ID of Cocktail` = `ingredients of cocktail`.`ID of Cocktail`
                        AND `Name of Ingredients` LIKE %s
                    )
                    """
                    records = data_db.find(sql_query, (f"%{ingredient.strip()}%",))
                    all_found_records += records

                record_counts = {record[0]: all_found_records.count(record) for record in all_found_records}

                final_duplicate_records = [record for record, count in record_counts.items() if count == len(exclude_ingredients)]

                if final_duplicate_records:
                    selected_records = random.sample(final_duplicate_records, min(3, len(final_duplicate_records)))
                    cocktail_names = [record for record in selected_records]    
                    cocktail_names_str = '、'.join(cocktail_names)
                    return {"Message": f"這是為你推薦不會過敏的調酒：{cocktail_names_str}", "Special": "#0"}
                else:
                    return {"Message":"沒有符合的調酒" ,"Special":"#0" }

            elif "做" in input_text[2:] or "作法" in input_text[2:]:
                return {"Message": "請輸入想做的調酒名稱:", "Special": "#2"}
            if "#2" in input_text:
                cocktail = input_text[4:]
                print("dsds",cocktail)
                methods = data_db.get_cocktail_production_method(cocktail)
                if methods:
                    # Join the list of methods into a single string and replace \r\n with a newline
                    formatted_methods = ''.join(methods).replace("\r\n", "").replace("\r", "").replace("\n", "")
                    return {"Message": f"該調酒做法為{formatted_methods}", "Special": "#0"}
                else:
                    return {"Message": "沒有符合的調酒", "Special": "#0"}


            elif "材料" in input_text[2:]:
                return {"Message":"請輸入材料和基酒（多個項目請用逗號分隔）：","Special":"#3" }
            if "#3" in input_text:
                input_str = input_text[4:]
                
                input_list = input_str.split(",")
                
                ingredients = []
                base_ingredients = []

                for item in input_list:
                    item = item.strip()
                 
                    base_ingredients.append(item)
                    ingredients.append(item)

                if not ingredients and not base_ingredients:
                    return {"Message":"請重新輸入","Special":"#0" }
                else:
                    conditions_ingredients_all = " AND ".join(["`ingredients of wine`.`Name of Ingredients` LIKE %s" for _ in ingredients]) if ingredients else None
                    conditions_base_all = " OR ".join(["`liquor`.`name of wine` LIKE %s" for _ in base_ingredients]) if base_ingredients else None

                    conditions_ingredients_any = " OR ".join(["`ingredients of wine`.`Name of Ingredients` LIKE %s" for _ in ingredients]) if ingredients else None

                    sql_query_all = None
                    params_all = []
                    if conditions_ingredients_all and conditions_base_all:
                        sql_query_all = f"""
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        JOIN `ingredients of cocktail` ON `cocktail list`.`ID of Cocktail` = `ingredients of cocktail`.`ID of Cocktail`
                        JOIN `ingredients of wine` ON `ingredients of cocktail`.`ID of Ingredients` = `ingredients of wine`.`ID of Ingredients`
                        LEFT JOIN `liquor` ON `cocktail list`.`ID of liquor` = `liquor`.`ID of Liquor`
                        WHERE {conditions_ingredients_all} AND ({conditions_base_all})
                        """
                        params_all = [f"%{ingredient}%" for ingredient in ingredients] + [f"%{base}%" for base in base_ingredients]
                    elif conditions_ingredients_all:
                        sql_query_all = f"""
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        JOIN `ingredients of cocktail` ON `cocktail list`.`ID of Cocktail` = `ingredients of cocktail`.`ID of Cocktail`
                        JOIN `ingredients of wine` ON `ingredients of cocktail`.`ID of Ingredients` = `ingredients of wine`.`ID of Ingredients`
                        WHERE {conditions_ingredients_all}
                        """
                        params_all = [f"%{ingredient}%" for ingredient in ingredients]
                    elif conditions_base_all:
                        sql_query_all = f"""
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        LEFT JOIN `liquor` ON `cocktail list`.`ID of liquor` = `liquor`.`ID of Liquor`
                        WHERE {conditions_base_all}
                        """
                        params_all = [f"%{base}%" for base in base_ingredients]

                    records_all = data_db.find(sql_query_all, params_all) if sql_query_all else []

                    sql_query_any = None
                    params_any = []
                    if conditions_ingredients_any and conditions_base_all:
                        sql_query_any = f"""
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        JOIN `ingredients of cocktail` ON `cocktail list`.`ID of Cocktail` = `ingredients of cocktail`.`ID of Cocktail`
                        JOIN `ingredients of wine` ON `ingredients of cocktail`.`ID of Ingredients` = `ingredients of wine`.`ID of Ingredients`
                        LEFT JOIN `liquor` ON `cocktail list`.`ID of liquor` = `liquor`.`ID of Liquor`
                        WHERE ({conditions_ingredients_any}) OR ({conditions_base_all})
                        """
                        params_any = [f"%{ingredient}%" for ingredient in ingredients] + [f"%{base}%" for base in base_ingredients]
                    elif conditions_ingredients_any:
                        sql_query_any = f"""
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        JOIN `ingredients of cocktail` ON `cocktail list`.`ID of Cocktail` = `ingredients of cocktail`.`ID of Cocktail`
                        JOIN `ingredients of wine` ON `ingredients of cocktail`.`ID of Ingredients` = `ingredients of wine`.`ID of Ingredients`
                        WHERE {conditions_ingredients_any}
                        """
                        params_any = [f"%{ingredient}%" for ingredient in ingredients]
                    elif conditions_base_all:
                        sql_query_any = f"""
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        LEFT JOIN `liquor` ON `cocktail list`.`ID of liquor` = `liquor`.`ID of Liquor`
                        WHERE {conditions_base_all}
                        """
                        params_any = [f"%{base}%" for base in base_ingredients]

                    records_any = data_db.find(sql_query_any, params_any) if sql_query_any else []

                    if records_any:
                        filtered_records_any = [record[0].strip() for record in records_any if record[0].strip()]
    
                        selected_records_any = random.sample(filtered_records_any, min(3, len(filtered_records_any)))
          
                        cocktail_names = '、'.join(selected_records_any)
                        return {"Message": f"這些材料可以做出以下調酒：{cocktail_names}", "Special": "#0"}
                    else:
                        return {"Message":"沒有符合的調酒","Special":"#0"}

            elif "最多按讚" in input_text[:2]:
                
                query = """
                SELECT `cocktail list`.`Name of Cocktail`, COUNT(`favorite cocktail`.`ID of Account`) AS favorite_count
                FROM `favorite cocktail`, `cocktail list`
                WHERE `cocktail list`.`ID of Cocktail` = `favorite cocktail`.`ID of Cocktail`
                GROUP BY `cocktail list`.`ID of Cocktail`
                ORDER BY favorite_count DESC
                LIMIT 1;
                """

                result = data_db.find(query)

                if result:
                    favorite_cocktail_id = result[0][0]
                    favorite_count = result[0][1]
                    return {"Message":f"推薦{favorite_cocktail_id}有{favorite_count}個使用者喜歡","Special":"#0" }
                    
                else:
                    return {"Message":"沒有符合的調酒","Special":"#0" }
                
            
            elif "酒量"  in input_text:
                if any(word in input_text for word in ["好", "大", "海", "行", "多", "棒", "優", "高","讚","無止盡","硬"]):
                    if any(word in input_text for word in ["不", "不太", "沒有", "沒","差", "爛", "菜", "廢", "嫩", "幹", "懶蛋", "遜", "低","小"]):
                        sql = """
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        WHERE `Low alcohol concentration` = '1'
                        """
                        records = data_db.find(sql)
                        filtered_records = []

                        for record in records:
                            
                            if record and record[0]:  
                                stripped_value = record[0].strip()
                                if stripped_value:
                                    filtered_records.append(stripped_value)
                        if filtered_records:
                            selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                            cocktail_names = '、'.join(selected_records)
                            return ({"Message": f"以下為你推薦三款酒精濃度低的調酒: {cocktail_names}", "Special": "#0"})  
                        else:
                            return ({"Message": "沒有符合的調酒", "Special": "#0"})
                        
                
                    sql = """
                    SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                    FROM `cocktail list`
                    WHERE `High alcohol concentration` = '1'
                    """
                    records = data_db.find(sql)
                    filtered_records = []

                    for record in records:
                        
                        if record and record[0]:  
                            stripped_value = record[0].strip()
                            if stripped_value:
                                filtered_records.append(stripped_value)
                    if filtered_records:
                        selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                        cocktail_names = '、'.join(selected_records)
                        return ({"Message": f"以下為你推薦三款酒精濃度高的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                    else:
                        return ({"Message": "沒有符合的調酒", "Special": "#0"})
                    
                if any(word in input_text for word in ["差", "爛", "菜", "廢", "嫩", "幹", "懶蛋", "遜", "低","小","錯"]):
                    if any(word in input_text for word in ["不", "不太", "沒有", "沒"]):
                        sql = """
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        WHERE `High alcohol concentration` = '1'
                        """
                        records = data_db.find(sql)
                        filtered_records = []

                        for record in records:
                            
                            if record and record[0]:  
                                stripped_value = record[0].strip()
                                if stripped_value:
                                    filtered_records.append(stripped_value)
                        if filtered_records:
                            selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                            cocktail_names = '、'.join(selected_records)
                            return ({"Message": f"以下為你推薦三款酒精濃度高的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                        else:
                            return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                        
                
                    sql = """
                    SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                    FROM `cocktail list`
                    WHERE `Low alcohol concentration` = '1'
                    """
                    records = data_db.find(sql)
                    filtered_records = []

                    for record in records:
                        
                        if record and record[0]:  
                            stripped_value = record[0].strip()
                            if stripped_value:
                                filtered_records.append(stripped_value)
                    if filtered_records:
                        selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                        cocktail_names = '、'.join(selected_records)
                        return ({"Message": f"以下為你推薦三款酒精濃度低的調酒: {cocktail_names}", "Special": "#0"})  
                    else:
                        return ({"Message": "沒有符合的調酒", "Special": "#0"})
                else:
                    query = """
                    SELECT `cocktail list`.`Name of Cocktail`, COUNT(`favorite cocktail`.`ID of Account`) AS favorite_count
                    FROM `favorite cocktail`, `cocktail list`
                    WHERE `cocktail list`.`ID of Cocktail` = `favorite cocktail`.`ID of Cocktail`
                    GROUP BY `cocktail list`.`ID of Cocktail`
                    ORDER BY favorite_count DESC
                    LIMIT 1;
                    """
                    result = data_db.find(query)

                    if result:
                        favorite_cocktail_id = result[0][0]
                        favorite_count = result[0][1]
                        return {"Message":f"推薦{favorite_cocktail_id}給您","Special":"#0" }
                        
                    else:
                        return {"Message":"沒有符合的調酒","Special":"#0" }
            else:
                input_seq = token.texts_to_sequences([list(jieba.cut(input_text, cut_all=True))])
                input_padded = sequence.pad_sequences(input_seq, maxlen=100)
                prediction = reload_model.predict(input_padded)
                predicted_class = np.argmax(prediction)
                #print(prediction, predicted_class)
            
                if predicted_class == 1:
                    return {"Message":"調酒網站不會有無酒精的","Special":"#0" }
                    
                elif predicted_class == 2:  
                    sql = """
                    SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                    FROM `cocktail list`
                    WHERE `Low alcohol concentration` = '1'
                    """
                    records = data_db.find(sql)
                    filtered_records = []

                    for record in records:
                        
                        if record and record[0]:  
                            stripped_value = record[0].strip()
                            if stripped_value:
                                filtered_records.append(stripped_value)
                    if filtered_records:
                        selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                        cocktail_names = '、'.join(selected_records)
                        return ({"Message": f"以下為你推薦三款酒精濃度低的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                    else:
                        return ({"Message": "沒有符合的調酒", "Special": "#0"})  
                        
                elif predicted_class == 3:  # 酒精濃度中的调酒
                    sql = """
                    SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                    FROM `cocktail list`
                    WHERE `Medium alcohol concentration` = '1'
                    """
                    records = data_db.find(sql)
                    filtered_records = []

                    for record in records:
                        
                        if record and record[0]:  
                            stripped_value = record[0].strip()
                            if stripped_value:
                                filtered_records.append(stripped_value)
                    if filtered_records:
                        selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                        cocktail_names = '、'.join(selected_records)
                        return ({"Message": f"以下為你推薦三款酒精濃度中的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                    else:
                        return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                        
                elif predicted_class == 4:  # 酒精濃度高的调酒
                    sql = """
                    SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                    FROM `cocktail list`
                    WHERE `High alcohol concentration` = '1'
                    """
                    records = data_db.find(sql)
                    filtered_records = []

                    for record in records:
                        
                        if record and record[0]:  
                            stripped_value = record[0].strip()
                            if stripped_value:
                                filtered_records.append(stripped_value)
                    if filtered_records:
                        selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                        cocktail_names = '、'.join(selected_records)
                        return ({"Message": f"以下為你推薦三款酒精濃度高的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                    else:
                        return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                        
                elif predicted_class == 5 or predicted_class == 0:
                    if any(word in input_text for word in ["糖", "甜"]):
                        if any(word in input_text for word in ["不", "沒","無"]):
                            sql = """
                            SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                            FROM `cocktail list`
                            WHERE `Sour` = '1' OR `bitter` = '1' OR `spicy` = '1' 
                            """
                            records = data_db.find(sql)
                            filtered_records = []

                            for record in records:
                                
                                if record and record[0]:  
                                    stripped_value = record[0].strip()
                                    if stripped_value:
                                        filtered_records.append(stripped_value)
                            if filtered_records:
                                selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                                cocktail_names = '、'.join(selected_records)
                                return ({"Message": f"以下為你推薦三款不含甜的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                            else:
                                return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                        sql = """
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        WHERE `Sweet` = '1'
                        """
                        records = data_db.find(sql)
                        filtered_records = []

                        for record in records:
                            
                            if record and record[0]:  
                                stripped_value = record[0].strip()
                                if stripped_value:
                                    filtered_records.append(stripped_value)
                        if filtered_records:
                            selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                            cocktail_names = '、'.join(selected_records)
                            return ({"Message": f"以下為你推薦三款甜的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                        else:
                            return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                    
                    if "苦" in input_text:
                        if any(word in input_text for word in ["不", "沒"]):
                            sql = """
                            SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                            FROM `cocktail list`
                            WHERE `Sour` = '1' OR `Sweet` = '1' OR `spicy` = '1' 
                            """
                            records = data_db.find(sql)
                            filtered_records = []

                            for record in records:
                                
                                if record and record[0]:  
                                    stripped_value = record[0].strip()
                                    if stripped_value:
                                        filtered_records.append(stripped_value)
                            if filtered_records:
                                selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                                cocktail_names = '、'.join(selected_records)
                                return ({"Message": f"以下為你推薦三款不含苦的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                            else:
                                return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                        sql = """
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        WHERE `bitter` = '1'
                        """
                        records = data_db.find(sql)
                        filtered_records = []

                        for record in records:
                            
                            if record and record[0]:  
                                stripped_value = record[0].strip()
                                if stripped_value:
                                    filtered_records.append(stripped_value)
                        if filtered_records:
                            selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                            cocktail_names = '、'.join(selected_records)
                            return ({"Message": f"以下為你推薦三款苦的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                        else:
                            return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                    
                    if "酸" in input_text:
                        if any(word in input_text for word in ["不", "沒"]):
                            sql = """
                            SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                            FROM `cocktail list`
                            WHERE `Sweet` = '1' OR `bitter` = '1' OR `spicy` = '1' 
                            """
                            records = data_db.find(sql)
                            filtered_records = []

                            for record in records:
                                
                                if record and record[0]:  
                                    stripped_value = record[0].strip()
                                    if stripped_value:
                                        filtered_records.append(stripped_value)
                            if filtered_records:
                                selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                                cocktail_names = '、'.join(selected_records)
                                return ({"Message": f"以下為你推薦三款不含酸的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                            else:
                                return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                        sql = """
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        WHERE `Sour` = '1'
                        """
                        
                        records = data_db.find(sql)
                        filtered_records = []

                        for record in records:
                            
                            if record and record[0]:  
                                stripped_value = record[0].strip()
                                if stripped_value:
                                    filtered_records.append(stripped_value)
                        if filtered_records:
                            selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                            cocktail_names = '、'.join(selected_records)
                            return ({"Message": f"以下為你推薦三款酸的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                        else:
                            return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                    
                    if "辣" in input_text:
                        if any(word in input_text for word in ["不", "沒"]):
                            sql = """
                            SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                            FROM `cocktail list`
                            WHERE `Sour` = '1' OR `bitter` = '1' OR `Sweet` = '1' 
                            """
                            records = data_db.find(sql)
                            filtered_records = []

                            for record in records:
                                
                                if record and record[0]:  
                                    stripped_value = record[0].strip()
                                    if stripped_value:
                                        filtered_records.append(stripped_value)
                            if filtered_records:
                                selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                                cocktail_names = '、'.join(selected_records)
                                return ({"Message": f"以下為你推薦三款不含辣的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                            else:
                                return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                        sql = """
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        WHERE `spicy` = '1'
                        """
                        records = data_db.find(sql)
                        filtered_records = []

                        for record in records:
                            
                            if record and record[0]:  
                                stripped_value = record[0].strip()
                                if stripped_value:
                                    filtered_records.append(stripped_value)
                        if filtered_records:
                            selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                            cocktail_names = '、'.join(selected_records)
                            return ({"Message": f"以下為你推薦三款辣的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                        else:
                            return ({"Message": "沒有符合的調酒", "Special": "#0"})  
                    else:
                        query = """
                        SELECT `cocktail list`.`Name of Cocktail`, COUNT(`favorite cocktail`.`ID of Account`) AS favorite_count
                        FROM `favorite cocktail`, `cocktail list`
                        WHERE `cocktail list`.`ID of Cocktail` = `favorite cocktail`.`ID of Cocktail`
                        GROUP BY `cocktail list`.`ID of Cocktail`
                        ORDER BY favorite_count DESC
                        LIMIT 1;
                        """
                        result = data_db.find(query)

                        if result:
                            favorite_cocktail_id = result[0][0]
                            favorite_count = result[0][1]
                            return {"Message":f"推薦{favorite_cocktail_id}給您","Special":"#0" }
                            
                        else:
                            return {"Message":"沒有符合的調酒","Special":"#0" }
                elif predicted_class == 6:
                    if any(word in input_text for word in ["不", "沒"]):
                        sql = """
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        WHERE `Hot` = '1' 
                        """
                        records = data_db.find(sql)
                        filtered_records = []

                        for record in records:
                            
                            if record and record[0]:  
                                stripped_value = record[0].strip()
                                if stripped_value:
                                    filtered_records.append(stripped_value)
                        if filtered_records:
                            selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                            cocktail_names = '、'.join(selected_records)
                            return ({"Message": f"以下為你推薦三款熱的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                        else:
                            return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                    sql = """
                    SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                    FROM `cocktail list`
                    WHERE `Ice` = '1'
                    """
                    records = data_db.find(sql)
                    filtered_records = []

                    for record in records:
                        
                        if record and record[0]:  
                            stripped_value = record[0].strip()
                            if stripped_value:
                                filtered_records.append(stripped_value)
                    if filtered_records:
                        selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                        cocktail_names = '、'.join(selected_records)
                        return ({"Message": f"以下為你推薦三款冰的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                    else:
                        return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                        
                elif predicted_class == 7:
                    if any(word in input_text for word in ["不", "沒"]):
                        sql = """
                        SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                        FROM `cocktail list`
                        WHERE `Ice`='1' 
                        """
                        records = data_db.find(sql)
                        filtered_records = []

                        for record in records:
                            
                            if record and record[0]:  
                                stripped_value = record[0].strip()
                                if stripped_value:
                                    filtered_records.append(stripped_value)
                        if filtered_records:
                            selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                            cocktail_names = '、'.join(selected_records)
                            return ({"Message": f"以下為你推薦三款冰的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                        else:
                            return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
                    sql = """
                    SELECT DISTINCT `cocktail list`.`Name of Cocktail`
                    FROM `cocktail list`
                    WHERE `Hot` = '1'
                    """
                    records = data_db.find(sql)
                    filtered_records = []

                    for record in records:
                        
                        if record and record[0]:  
                            stripped_value = record[0].strip()
                            if stripped_value:
                                filtered_records.append(stripped_value)
                    if filtered_records:
                        selected_records = random.sample(filtered_records, min(3, len(filtered_records)))
                        cocktail_names = '、'.join(selected_records)
                        return ({"Message": f"以下為你推薦三款熱的調酒: {cocktail_names}", "Special": "#0"})  # 使用 print 代替 return 進行調試
                    else:
                        return ({"Message": "沒有符合的調酒", "Special": "#0"}) 
        except:
            {"Message": "再試一次", "Special": "#0"}
            
    