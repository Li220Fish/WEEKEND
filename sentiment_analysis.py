from keras.models import load_model
import jieba
from tensorflow.keras.preprocessing.sequence import pad_sequences
from token_help import test
import re

def mood_analy(text):
    # 检查文本是否包含英文或数字
    if re.search('[a-zA-Z0-9]', text):
        return (0, None)

    # 定义关键词
    negative_words = ["差", "爛", "討厭", "遜", "低", "小"]
    negation_words = ["不", "好難"]
    positive_words = ["喜歡", "愛", "適合", "好喝", "喝"]

    # 检查文本中的关键词和否定词
    if any(word in text for word in negative_words):
        if any(word in text for word in negation_words):
            return (0.91486, "正面")
    
    if any(word in text for word in positive_words):
        if any(word in text for word in negation_words):
            return (0.92384, "負面")
    
    # 分词处理
    processed_text = jieba.lcut(text)
    
    # 将文本转换为数字序列
    tokenizer = test()
    max_length = 50
    processed_input = tokenizer.texts_to_sequences([processed_text])
    
    # 填充序列至固定长度
    processed_input = pad_sequences(processed_input, maxlen=max_length)
    
    # 载入模型
    model = load_model("my_model_final.h5")
    
    # 使用模型进行预测
    prediction = model.predict(processed_input)[0]
    
    # 判断情感
    if prediction[1] > prediction[0]:
        result = (prediction[1], "正面")
    else:
        result = (prediction[0], "负面")
    
    return result