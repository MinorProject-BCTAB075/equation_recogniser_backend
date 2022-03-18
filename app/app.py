from flask import Blueprint, request, json, jsonify

views = Blueprint('views', __name__)

@views.route('/predict', methods=["GET", "POST"])
def predict():
    d={}
    if request.method =="POST":
	# var input = imageFile;
	
	# var output = ["answer string here"]
        return jsonify(["Register success"])