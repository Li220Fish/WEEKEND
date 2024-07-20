import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding, LSTM
import jieba
import os

# 定義處理文本的函數，將文本轉換為序列並填充到固定長度
def process_text(text, token, maxlen=50):
    text_seq = token.texts_to_sequences([text])
    padded_seq = pad_sequences(text_seq, maxlen=maxlen)
    return padded_seq

# 加載停用詞列表
def load_stopwords():
    current_path = os.path.abspath(__file__)
    directory = os.path.dirname(current_path)
    wordstop_path = os.path.join(directory, 'wordstop.txt')
    with open(wordstop_path, 'r', encoding='utf8') as f:
        stopWords = f.read().split('\n')
    stopWords.append('\n')
    return stopWords

# 調用函數加載停用詞
stopWords = load_stopwords()

# 讀取訓練數據
with open("training_data_final.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# 創建一個長度為225的數組，初始化為1
array = np.ones(247)
# 在數組後面添加111個0
array = np.concatenate([array, np.zeros(176)])
y_train = array

# 將文本和標籤組合成元組列表，並打亂順序
data_tuples = list(zip(lines, y_train))
np.random.shuffle(data_tuples)
shuffled_texts, shuffled_labels = zip(*data_tuples)

# 將文本和標籤轉換為 numpy 數組
x_train = np.array(shuffled_texts)
y_train = np.array(shuffled_labels)
y_train = y_train.astype(int)
y_train = to_categorical(y_train, 2)  # 將標籤轉換為 one-hot 編碼格式

sentence = []
# 使用 jieba 分詞將每個文本分成單字
for content in x_train:
    _sentence = list(jieba.cut(content, cut_all=True))
    sentence.append(_sentence)

remainderWords2 = []
# 移除停用詞
for content in sentence:
    remainderWords2.append(list(filter(lambda a: a not in stopWords, content)))

print(remainderWords2)
# 建立中文字典，將文字轉換成數字（取最常用的3000個字）
token = Tokenizer(num_words=3000)
token.fit_on_texts(remainderWords2)

# 將分詞後的文本轉換為數字序列，並填充長度為50
x_train_seq = token.texts_to_sequences(remainderWords2)
x_train = pad_sequences(x_train_seq, maxlen=50)
print(x_train.shape)  # 打印 x_train 的形狀

# 建立模型
model = Sequential()
model.add(Embedding(output_dim=64, input_dim=3000, input_length=50))
model.add(LSTM(units=32))
model.add(Dropout(0.1))
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=2, activation='sigmoid'))
model.summary()

# 編譯模型
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 訓練模型
train_history = model.fit(x_train, y_train, 
                          batch_size=64, 
                          epochs=14, 
                          verbose=2, 
                          validation_split=0.2)

# 保存模型
model.save('my_model_final.h5')
