# global definitions for all files
import os
import numpy as np


import tensorflow as tf
from tensorflow import keras

# path definitions
# MAIN_DIR = ".."
# DATA_DIR = os.path.join(MAIN_DIR,"dataset")
# MODEL_DIR = os.path.join(MAIN_DIR,"Models")
# FIG_DIR = os.path.join(MAIN_DIR,"Figures")
# os.makedirs(FIG_DIR,exist_ok=True)
# os.makedirs(MODEL_DIR,exist_ok=True)

# variable definitions
LABELS = ["ZERO","ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE"]
SAMPLE_RATE = SR = 8000 #Hz
LENGTH = 4096 #default sample length

# mfcc parameters
n_mfcc=20
hop_length=125
n_fft=256
