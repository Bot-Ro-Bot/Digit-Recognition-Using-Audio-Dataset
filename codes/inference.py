import imp
from types import LambdaType

from keras.models import Model
from numpy import lib
from numpy.lib.function_base import select
from config import *

import librosa
class _Inference:
    """
    What? -> Singleton class: a class that can have only one instance
    Why? -> We only need one instance of this class used as an end point in a Flask App. 
         -> To ensure only one instance of this class is created
    """
    model = None

    _instance = None
    
    def extract_features(self,path):
        audio, _ = librosa.load(path)
        if(len(audio)>LENGTH):
            audio = audio[:LENGTH]
        else:
            audio = np.pad(audio,(0,LENGTH-len(audio)),constant_values=(0,0))

        mfcc = librosa.feature.mfcc(audio,sr=SR,n_mfcc=n_mfcc,hop_length=hop_length,n_fft=n_fft)
        return mfcc.T

    def predict(self,path):
        # extract features
        mfcc = self.extract_features(path)
       
        # reshape array to 4d array
        mfcc = mfcc[np.newaxis, ... , np.newaxis]
       
        # make prediction
        prediction = np.argmax (self.model.predict(mfcc))
        
        return LABELS[int(prediction)]

def Inference():
    if _Inference._instance is None:
        # if instance is not created, create one
        _Inference._instance = _Inference()
        try:
            _Inference.model = keras.models.load_model(os.path.join(MODEL_DIR,"model.h5"))
        except Exception as ex:
            print("Model Load Failed due to: ",ex)
    return _Inference._instance


if __name__== "__main__":
    inf = Inference()
    print(inf.predict("/home/deadpool/github/MNIST-Audio-Classification/7_jackson_1.wav"))
