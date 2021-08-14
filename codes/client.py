
#index.html maa ni garna milxa hai yo sabbai kura 

import requests

URL = "http://127.0.0.1:5000/predict"

FILE_PATH = "../test/one.wav"

if __name__=="__main__":
    audio = open(FILE_PATH,"rb")
    values = {"file":(FILE_PATH,audio,"audio/wav")}
    
    # request service from server through post (and sending file)
    response = requests.post(URL,files=values)
    
    # received response from server
    data = response.json()
    print("Prediction: ",data["label"])
