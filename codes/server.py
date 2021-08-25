import random
from flask import Flask, json, jsonify, request, render_template
from inference import Inference
import os
from audio import *
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

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



@app.route("/record",methods=["POST","GET"])
def record():
    """
    record data and return the numpy array for prediction
    """
    audio, save_audio = get_audio()
    audio = audio.flatten()
    save_audio()
    inf = Inference()

    prediction = inf.predict(audio)

    data= {"label":prediction}
  
    return prediction

if __name__ == "__main__":
    # run flask app
    # app.run(debug=False)
    app.run(debug=True)
