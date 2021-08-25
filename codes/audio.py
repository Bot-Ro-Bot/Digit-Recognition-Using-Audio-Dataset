from sys import path
import sounddevice as sd
import os
from scipy.io.wavfile import write,read

from config import INFER_DIR
import tqdm
import time

SAMPLING_FREQUENCY = SR = 8000
DURATION = 1
MONO = 1
STEREO = 2

sd.default.samplerate = SR
sd.default.channels = MONO

def get_audio(name="audio.wav",CHANNELS=MONO,duration=DURATION):

    print("Get ready to say a diigt !!!")
    for i in range(3,-1,-1):
        time.sleep(1)
        print(i)
    print("Start !!")
    recording = sd.rec(int(duration * SR), 
                    samplerate=SR, channels=CHANNELS)

    for i in tqdm.tqdm(range(duration*4),desc="Recording "):
        time.sleep(0.25)
    sd.wait()
  
    def save_audio():
        try:
            abc = len(os.listdir(INFER_DIR))
            name = str(abc)+".wav"
            print("Saving recording as: ",name)
            write(os.path.join(INFER_DIR,name), SR, recording)
            print("Recording saved.")
        except Exception as ex:
            print("Recording failed due to ", ex)
    
    return recording,save_audio


if __name__=="__main__":
    _ , save = get_audio()
    save()