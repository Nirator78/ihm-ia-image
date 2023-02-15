import os
from flask import Flask, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename

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
    return render_template("index.html", user_image = "http://localhost:5000/get-image/"+filename, lettre="A")