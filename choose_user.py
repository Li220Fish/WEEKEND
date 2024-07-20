from collections import Counter
from SQL import DataBase

def get_user_favorite_cocktails(data_db, user_id):
    """
    查詢特定用戶喜歡的雞尾酒代號。

    參數:
    data_db (DataBase): 資料庫連接。
    user_id (str): 用戶ID。

    返回:
    list: 用戶喜歡的雞尾酒ID列表。
    """
    try:
        sql = """
        SELECT `ID of Cocktail`
        FROM `favorite cocktail`
        WHERE `ID of Account` = %s
        """
        
        results = data_db.find(sql, (user_id,))
        
        user_favorites = [row[0] for row in results]

        return user_favorites
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def get_cocktail_details(data_db, cocktail_ids):
    """
    查詢雞尾酒詳細信息。

    參數:
    data_db (DataBase): 資料庫連接。
    cocktail_ids (list): 雞尾酒ID列表。

    返回:
    list: 雞尾酒詳細信息列表。
    """
    try:
        sql = """
        SELECT `ID of Cocktail`, 
               `Low alcohol concentration`,
               `Medium alcohol concentration`,
               `High alcohol concentration`,
               `Sour`, `Sweet`, `Bitter`, `Spicy`,
               `Ice`, `Hot`
        FROM `cocktail list`
        WHERE `ID of Cocktail` IN (%s)
        """ % ','.join(['%s'] * len(cocktail_ids))
        results = data_db.find(sql, cocktail_ids)

        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def count_attributes(cocktail_details):
    """
    統計每個屬性的出現次數。

    參數:
    cocktail_details (list): 雞尾酒詳細信息的列表。

    返回:
    dict: 每個屬性的出現次數。
    """
    attribute_counts = Counter()

    for details in cocktail_details:
        attributes = {
            'Low alcohol concentration': details[1],
            'Medium alcohol concentration': details[2],
            'High alcohol concentration': details[3],
            'Sour': details[4],
            'Sweet': details[5],
            'Bitter': details[6],
            'Spicy': details[7],
            'Ice': details[8],
            'Hot': details[9],
        }

        for attribute, value in attributes.items():
            if value is not None:
                attribute_counts[attribute] += 1

    return attribute_counts

def get_top_n_attributes(attribute_counts, n=3):
    """
    獲取出現次數最多的前N個屬性。

    參數:
    attribute_counts (dict): 每個屬性的出現次數。
    n (int): 要獲取的前N個屬性。

    返回:
    list: 出現次數最多的前N個屬性。
    """
    sorted_attributes = sorted(attribute_counts.items(), key=lambda x: (-x[1], x[0]))
    top_attributes = sorted_attributes[:n]

    return top_attributes

def get_user_label_score(top_attributes):
    """
    根據前三高的屬性計算用戶標籤得分。

    參數:
    top_attributes (list): 前三高的屬性列表。

    返回:
    dict: 用戶標籤得分。
    """
    score = {'重酒精': 0, '大眾味': 0, '獨特喜好': 0}

    for attr in top_attributes:
        if attr[0] in {'High alcohol concentration', 'Medium alcohol concentration', 'Ice'}:
            score['重酒精'] += 1
        if attr[0] in {'Sour', 'Sweet', 'Low alcohol concentration'}:
            score['大眾味'] += 1
        if attr[0] in {'Spicy', 'Bitter', 'Sour'}:
            score['獨特喜好'] += 1

    return score

def get_user_label(top_attributes):
    """
    根據得分最高的標籤來決定用戶的標籤。

    參數:
    top_attributes (list): 前三高的屬性列表。

    返回:
    str: 用戶標籤。
    """
    user_label_score = get_user_label_score(top_attributes)
    user_label = max(user_label_score, key=user_label_score.get)
    return user_label

def assign_user_labels(user_id, data_db):
    """
    為特定用戶分配標籤。

    參數:
    user_id (str): 用戶ID。
    data_db (DataBase): 資料庫連接。
    """
    user_favorites = get_user_favorite_cocktails(data_db, user_id)
    if not user_favorites:
        return("無喜好",['None','None','None'])

    cocktail_details = get_cocktail_details(data_db, user_favorites)
    attribute_counts = count_attributes(cocktail_details)
    top_attributes = get_top_n_attributes(attribute_counts)
    user_label = get_user_label(top_attributes)
    top_labels = [attr[0] for attr in top_attributes]
    return(user_label,top_labels)
    #print(f"User ID: {user_id}, Label: {user_label}, Top Attributes: {top_labels}")


    data_db = DataBase()
    assign_user_labels(user_id, data_db)
