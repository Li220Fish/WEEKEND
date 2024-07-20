from collections import Counter
from SQL import DataBase

def get_all_users_favorite_cocktails():
    try:
        # 查询所有用户及其喜欢的鸡尾酒代号
        sql = """
        SELECT `ID of Account`, `ID of Cocktail`
        FROM `favorite cocktail`
        """
        
        results = data_db.find(sql)
        
        user_favorites = {}
        for account_id, cocktail_id in results:
            if account_id not in user_favorites:
                user_favorites[account_id] = []
            user_favorites[account_id].append(cocktail_id)

        return user_favorites
    except Exception as e:
        print(f"Error: {str(e)}")
        return {}

def get_cocktail_details(cocktail_ids):
    try:
        # 查询鸡尾酒详细信息
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
    sorted_attributes = sorted(attribute_counts.items(), key=lambda x: (-x[1], x[0]))
    top_attributes = sorted_attributes[:n]
    return top_attributes

def get_user_label(top_attributes):
    common_attributes = {attr[0] for attr in top_attributes}

    if common_attributes == {'High alcohol concentration', 'Medium alcohol concentration', 'Ice'}:
        user_label = "癮君子"
    elif common_attributes == {'Low alcohol concentration', 'Sweet', 'Sour'}:
        user_label = "愛妹酒"
    elif common_attributes == {'Spicy', 'Bitter', 'Sour'}:
        user_label = "重口味"
    else:
        user_label = "其他"

    print("判定的标签类型:", user_label)

    return user_label

def get_user_label_score(top_attributes):
    score = {'癮君子': 0, '愛妹酒': 0, '重口味': 0}

    for attr in top_attributes:
        if attr[0] == 'High alcohol concentration':
            score['癮君子'] += 1
        elif attr[0] == 'Low alcohol concentration':
            score['愛妹酒'] += 1
        elif attr[0] == 'Spicy':
            score['重口味'] += 1

    return score

def get_user_label(top_attributes):
    
    user_label_score = get_user_label_score(top_attributes)
    user_label = max(user_label_score, key=user_label_score.get)
    return user_label

def get_all_cocktail_labels(data_db):
    try:
        # 查询所有鸡尾酒的属性
        sql = """
        SELECT DISTINCT
            `Low alcohol concentration`,
            `Medium alcohol concentration`,
            `High alcohol concentration`,
            `Sour`, `Sweet`, `Bitter`, `Spicy`,
            `Ice`, `Hot`
        FROM `cocktail list`
        """

        results = data_db.find(sql)

        all_labels = set()
        for details in results:
            labels = [detail for detail in details if detail is not None]
            all_labels.update(labels)

        return all_labels
    except Exception as e:
        print(f"Error: {str(e)}")
        return set()

def get_common_labels(user_label, all_labels):
    
    if user_label == "癮君子":
        common_labels = {'High alcohol concentration', 'Medium alcohol concentration', 'Ice'} & all_labels
    elif user_label == "愛妹酒":
        common_labels = {'Low alcohol concentration', 'Sweet', 'Sour'} & all_labels
    elif user_label == "重口味":
        common_labels = {'Spicy', 'Bitter', 'Sour'} & all_labels
    else:
        common_labels = set()

    return common_labels

def assign_user_labels(user_favorites, data_db):
    all_labels = get_all_cocktail_labels(data_db)
    for user_id, cocktail_ids in user_favorites.items():
        cocktail_details = get_cocktail_details(data_db, cocktail_ids)
        attribute_counts = count_attributes(cocktail_details)
        top_attributes = get_top_n_attributes(attribute_counts)
        user_label = get_user_label(top_attributes)
        common_labels = get_common_labels(user_label, all_labels)
        return user_label
        #print(f"User ID: {user_id}, Label: {user_label}, Common Labels: {common_labels}")

if __name__ == "__main__":
    data_db = DataBase()
    print(data_db)
    user_favorites = get_all_users_favorite_cocktails(data_db)
    assign_user_labels(user_favorites, data_db)
