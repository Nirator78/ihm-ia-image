import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization

# Chemin vers les dossiers contenant les images
folder_path = "./data5g"

# Liste des classes
class_names = [
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

# Taille des images
image_size = (64, 64)

# Chargement des images et étiquettes
X = []
y = []
for i, class_name in enumerate(class_names):
    class_path = os.path.join(folder_path, class_name)
    for file_name in os.listdir(class_path):
        image_path = os.path.join(class_path, file_name)
        image = cv2.imread(image_path)
        image = cv2.resize(image, image_size)
        X.append(image)
        y.append(i)
        print(image_path)

# Conversion en tableaux NumPy
X = np.array(X)
y = np.array(y)

# Diviser les données en ensembles d'entraînement et de test
# random_state force le découpage et evite les écarts abérants
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lb = LabelBinarizer()
y_train = lb.fit_transform(y_train)

num_classes = len(class_names)

model = Sequential()
model.add(Conv2D(32, (3, 3), padding="same",input_shape=(64,64,3), activation="relu"))
# ingnore 30% de ce que dis la couche d'au dessus, moins d'overfit
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Conv2D(90, (3, 3), padding="same", activation="relu"))
# ingnore 30% de ce que dis la couche d'au dessus, moins d'overfit
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(90, (3, 3), padding="same", activation="relu"))
# ingnore 30% de ce que dis la couche d'au dessus, moins d'overfit
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(60, activation="relu"))
# reformate les données sous forme de "ligne" car Dense n'accepte pas les tableaux en entrée
model.add(Flatten())

model.add(Dense(40, activation="relu"))
model.add(Dense(num_classes, activation="softmax"))
model.summary()

# Compiler le modèle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entraîner le modèle
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2)

# export du modèle
model.save("CNN.h5")
model.save_weights("CNNWeights.h5")