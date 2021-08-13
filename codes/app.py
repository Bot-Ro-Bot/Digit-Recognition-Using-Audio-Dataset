from re import DEBUG
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello World</h1>"

@app.route("/predict")
def predict():
    return "predict page"

if __name__== "__main__":
    app.run(debug=True)