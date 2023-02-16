import os
from flask import Flask, request, redirect, render_template, send_file
from sklearn.preprocessing import LabelBinarizer
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
from PIL import Image
from tensorflow.keras import preprocessing
from sklearn.metrics import classification_report

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello_world():
    return "Hello World !"
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image/create', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("http://localhost:5000/infos/"+filename)
        
    return render_template("form.html")
        
@app.route('/get-image/<filename>')
def display_image(filename):
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(full_filename)

@app.route('/infos/<filename>')
def infos_for_image(filename):
    # Mettre ici le programme IA pour retourner la lettre
    model = load_model('CNNINSHALLAH.h5')
    print(model.summary())
    # model.load_weights('model/CNNWeights_1.h5')


    img_to_retrain = []

    i = 10
    for count in range(5) :
        img_temp = cv2.imread("./asl_dataset/0/hand1_0_bot_seg_"+str(count+1)+"_cropped.jpeg")
        img_temp = cv2.resize(img_temp, (64,64))
        # img_temp = Image.open()
        # img_temp = img_temp.resize((64,64))
        # img_temp = np.array(img_temp).astype(int)
        # print(img_temp.shape)
        img_to_retrain.append(img_temp)
    # print(len(img_to_retrain))
    img_to_retrain = np.array(img_to_retrain)
    print(type(img_to_retrain))
    y_pred = model.predict(img_to_retrain, verbose=1)
    y_pred = np.argmax(y_pred, axis=1)
    print(classification_report([26,26,26,26,26], y_pred))
    print(y_pred)

    # image = Image.open("./images/"+filename)
    image = cv2.imread("./images/"+filename)
    image = cv2.resize(image, (64,64))
    imageArray = [image]
    imageArray = np.array(imageArray)
    # test_image2 = image.resize((64,64))

    # test_image2 = preprocessing.image.img_to_array(test_image2)


    # # test_image = test_image / 255
    # test_image = np.expand_dims(test_image, axis =0)

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
        
    predictions = model.predict(imageArray)
    scores = tf.nn.softmax(predictions[0])
    scores = scores.numpy()
    print(scores)
    image_class = class_names[np.argmax(scores)]
    # print(image_class)

    return render_template("index.html", user_image = "http://localhost:5000/get-image/"+filename, lettre=image_class)