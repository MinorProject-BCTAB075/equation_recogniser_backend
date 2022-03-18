from flask import Blueprint, request, json, jsonify

views = Blueprint('views', __name__)

@views.route('/register', methods=["GET", "POST"])
def register():
    d={}
    if request.method =="POST":
        return jsonify(["Register success"])

@views.route('/login', methods=["GET", "POST"])
def login():
    d = {}
    if request.method =="POST":
        return jsonify([ "success"])