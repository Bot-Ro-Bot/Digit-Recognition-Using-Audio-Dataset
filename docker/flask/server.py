import random
from flask import Flask, json, jsonify, request
from inference import Inference
import os

app = Flask(__name__)

@app.route("/predict",methods=["POST"])
def predict():
    """
    predict function is an end point to this API to make a prediction and return it
    """
    # get an audio file from a client through POST request and save it
    audio = request.files["file"]
    filename = str(random.randint(0,1000))
    audio.save(filename)

    # making an inference of the model through singleton inference class
    inf = Inference()

    prediction = inf.predict(filename)
    os.remove(filename)

    data= {"label":prediction}
    return jsonify(data)


if __name__ == "__main__":
    # run flask app
    app.run(debug=False)