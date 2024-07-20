import numpy as np
import os
import jieba
from tensorflow.keras.preprocessing.text import Tokenizer

def load_stopwords():
    # 取得當前執行檔案的絕對路徑
    current_path = os.path.abspath(__file__)
    
    # 獲取所在目錄的路徑
    directory = os.path.dirname(current_path)
    
    # 構建 'wordstop.txt' 檔案的完整路徑
    wordstop_path = os.path.join(directory, 'wordstop.txt')
    
    # 打開 'wordstop.txt' 檔案並讀取停用詞
    with open(wordstop_path, 'r', encoding='utf8') as f:
        stopWords = f.read().split('\n')
        
    stopWords.append('\n')
    
    return stopWords

def test():

# 讀取文本檔案並存儲為列表
    with open("training_data_final.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

# 將文本轉換為 numpy array
    stopWords = load_stopwords()    
    x_train = np.array(lines)
    array = np.ones(247)

    # 将后面的部分置为 0
    array = np.concatenate([array, np.zeros(174)])
    y_train = array
    #把標籤設定成固定格式[0,1](這樣是1)，[1,0](這樣是0)
    from tensorflow.python.keras.utils import np_utils
    y_train = np_utils.to_categorical(y_train, 2)

    sentence=[]

    #透過jieba分詞工具，把自分成一個一個單字
    for content in x_train:
        _sentence=list(jieba.cut(content, cut_all=True))
        sentence.append(_sentence)

    remainderWords2 = []

    #如果裡面有停用詞，將其移除
    for content in sentence:
        remainderWords2.append(list(filter(lambda a: a not in stopWords, content)))

    #建立中文字典，把文字轉換成數字(取最常使用到的3000個字)
    token = Tokenizer(num_words=3000)
    token.fit_on_texts(remainderWords2)
    
    return token

a = test()
    