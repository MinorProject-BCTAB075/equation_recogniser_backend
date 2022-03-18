import os

from flask import Blueprint, request, json, jsonify
from werkzeug.utils import secure_filename  

from utils import predict_image

views = Blueprint('views', __name__)

image_store_folder =""#directory of the stored images relative to utils.py
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/predict', methods=["GET", "POST"])
def predict():
    d={}
    if request.method =="POST":
        if 'file' in request.files: #here file is the name of the input through which the uploaded image is accessed
            
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                #flash('No selected file')
                #handle no file uploaded
                pass

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                #secure_filename : Pass it a filename and it will return a secure version of it

                file.save(os.path.join(image_store_folder, filename))
                
                detected_exp = predict_image(image_store_folder+filename)
                # var output = ["answer string here"]
                return jsonify([detected_exp])