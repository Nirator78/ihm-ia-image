import os
import cv2
import numpy as np
from keras.models import load_model
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

model_path = "the_best_model.h5"

folder_path = "./data5g_cleaned"

X = []
Y = []

labels = [
    "A", "B", "C",
    "D", "E", "F",
    "G", "H", "I",
    "J", "K", "L",
    "M", "N", "O",
    "P", "Q", "R",
    "S", "T", "U",
    "V", "W", "X",
    "Y", "Z", "0",
    "1", "2", "3",
    "4", "5", "6",
    "7", "8", "9"
]

for label in labels:
    folderpath = os.path.join(folder_path, label)
    index = 0
    for file in os.listdir(folderpath):
        print(file)
        index += 1
        if index == 200:
            break
        img_path = os.path.join(folderpath, file)
        img = cv2.imread(img_path)
        X.append(np.array(img))
        Y.append(labels.index(label))
        
X = np.array(X)
Y = np.array(Y)

model = load_model(model_path)

X_train,X_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
model.fit(X_train,y_train, epochs=10, validation_data=(X_test,y_test))

# export du modèle
model.save("the_best_model_trained.h5")
model.save_weights("the_best_model_trained_weights.h5")