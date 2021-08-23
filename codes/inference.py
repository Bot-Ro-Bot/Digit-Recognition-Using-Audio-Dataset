from requests.api import get
from config import *
from audio import *
import librosa

class LoadModelError(Exception):
    pass

class _Inference:
    """
    What? -> Singleton class: a class that can have only one instance
    Why? -> We only need one instance of this class used as an end point in a Flask App. 
         -> To ensure only one instance of this class is created
    """
    model = None

    _instance = None
    
    def extract_features(self,file):

        if(isinstance(file,str)):
            audio, _ = librosa.load(file,sr=None)
        else:
            audio = file

        # if(not_path):
        #     audio = not_path
        # else:
        #     audio, _ = librosa.load(path,sr=None)
        
        # audio, _ = librosa.effects.trim(audio,top_db=20,frame_length=256, hop_length=64)

        if(len(audio)>LENGTH):
            audio = audio[:LENGTH]
        elif(len(audio)<LENGTH):
            audio = np.pad(audio,(0,LENGTH-len(audio)),constant_values=(0,0))

        mfcc = librosa.feature.mfcc(audio,sr=SR,n_mfcc=n_mfcc,hop_length=hop_length,n_fft=n_fft)
        return mfcc.T

    def predict(self,*args):
        # file = kwargs.values()[0]
        file = args[0]

        # extract features
        mfcc = self.extract_features(file)
       
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
            _Inference.model = keras.models.load_model(os.path.join(MODEL_DIR,"model5.h5"))

            if (_Inference.model == None):
                raise LoadModelError("Model path error. Model not found. Model is none.")
       
        except Exception as ex:
            print("Model Load Failed due to: ",ex)
    return _Inference._instance

if __name__== "__main__":
    inf = Inference()
    audio, save_audio = get_audio()
    # print(audio.flatten().shape)
    # print(inf.predict("../captured_audios/audio.wav"))
    print(inf.predict(audio.flatten()))
    if((input("Press y to save audio file or any other key quit.")).lower()=="y"):
        save_audio()

    # print(inf.predict("../test/zero.wav"))
    # print(inf.predict("../test/one.wav"))
    # print(inf.predict("../test/two.wav"))
    # print(inf.predict("../test/three.wav"))
    # print(inf.predict("../test/four.wav"))
    # print(inf.predict("../test/five.wav"))
    # print(inf.predict("../test/six.wav"))
    # print(inf.predict("../test/seven.wav"))
    # print(inf.predict("../test/eight.wav"))
    # print(inf.predict("../test/nine.wav"))
