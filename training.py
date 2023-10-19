import random
import json
import pickle
import numpy as np
import tensorflow as tf
from pyvi import ViTokenizer

data= json.loads(open('data.json', encoding='utf-8').read())

tu=[]
danh_sach=[]
nhan=[]
tu_ngat = ['?', '!', '.', ',', 'à', 'thì', 'mà', 'hãy', 'cho', '']


for i in data['du_lieu']:
    for mau_cau in i['mau_cau']:
        lst = ViTokenizer.tokenize(mau_cau).lower().split(' ')
        tu.extend(lst)
        danh_sach.append((lst,i['tag']))
        if i['tag'] not in nhan:
            nhan.append(i['tag'])


tu = [i for i in tu if i not in tu_ngat]
tu=sorted(set(tu))
nhan=sorted(set(nhan))


pickle.dump(tu,open('tu.pkl','wb'))
pickle.dump(nhan,open('nhan.pkl','wb'))

training =[]
outputEmpty=[0] * len(nhan)

for i in danh_sach:
    bag=[]
    MauCau = i[0]
    for a in tu:
        bag.append(1) if a in MauCau else bag.append(0)
    outputRow = list(outputEmpty)
    outputRow[nhan.index(i[1])] = 1
    training.append(bag + outputRow)
for i in training:
    print (i)
random.shuffle(training)


for i in training:
    print(i)
training=np.array(training)


trainX = training[:, :len(tu)]
trainY = training[:, len(tu):]



model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(trainX, trainY, epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5')
print('Done')