import os
import cv2
import numpy as np
from keras.models import load_model

# Charger le modèle de réseau de neurones pré-entraîné
model = load_model('CNN.h5')

# Chemin vers le dossier contenant les images
path = 'test/'

# Liste des lettres de l'alphabet
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Préparer les données pour l'inférence
data = []
for letter in letters:
    img_path = os.path.join(path, letter + '_test.jpg')
    img = cv2.imread(img_path)
    img = cv2.resize(img, (64, 64))
    data.append(img)
data = np.array(data, dtype="float") / 255.0

# Faire la prédiction
preds = model.predict(data)

# Afficher les résultats
correct = 0
for i, letter in enumerate(letters):
    pred_letter = letters[np.argmax(preds[i])]
    if letter == pred_letter:
        correct += 1
    print(f'Image {letter}: prediction = {pred_letter}')

# Calculer le taux de précision
accuracy = correct / len(letters) * 100
print(f'Taux de précision : {accuracy:.2f}%')