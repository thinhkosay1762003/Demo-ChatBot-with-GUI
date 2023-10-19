import random
import json
import pickle
import numpy as np
import task

from keras.models import load_model
from pyvi import ViTokenizer
import threading

window_size = "700x800"
data = json.loads(open('data.json', encoding='utf-8').read())
tu=pickle.load(open('tu.pkl', 'rb'))
nhan=pickle.load(open('nhan.pkl', 'rb'))
model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words=ViTokenizer.tokenize(sentence).split(' ')
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag= [0] * len(tu)
    for w in sentence_words:
        for i,word in enumerate(tu):
            if word==w:
                bag[i]=1
    return np.array(bag)

def predict_class(sentence):
    bow=bag_of_words(sentence)
    res=model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD =0.25
    print (res)
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
    print(results)
    results.sort(key=lambda x: x[1], reverse = True)
    return_list = []
    for r in results:
        return_list.append({'data':nhan[r[0]], 'probability': str(r[1])})
    return return_list
def get_response(intents_list, data_json,message):
    tag=intents_list[0]['data']
    danh_sach_chu_de = data_json['du_lieu']
    list_of_task = data_json['nhiem_vu']
    for i in list_of_task:
        if i['tag'] == tag:
            answer = eval(f"task.{i['mission']}('{message}')")
            return answer
            break
    for i in danh_sach_chu_de:
         if i['tag'] == tag:
            print(i['tag'])
            if len(i['tra_loi']) != 0:
                return random.choice(i['tra_loi'])
            break

if __name__ == "__main__":
    print("Chatbot đã sẵn sàng")