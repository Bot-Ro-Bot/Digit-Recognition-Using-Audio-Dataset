# importing necessary modules

from _typeshed import OpenTextMode
import os
import pickle

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Flatten, Conv2D, BatchNormalization, GlobalAveragePooling2D, MaxPool2D, Dense


def get_data():
    X = pickle.load(open("X","rb"))
    Y = pickle.load(open("Y","rb"))
    return X,Y

def process_data():
    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(labels).astype('float64')
    X = np.array(features)
    Y = encoded_labels


    splitter = StratifiedShuffleSplit(n_splits=1,test_size=0.1, random_state=42)

    train_id, test_id = next(splitter.split(X,Y))
    X_train,y_train,X_test,y_test = X[train_id],Y[train_id],X[test_id],Y[test_id]

    train_id, test_id = next(splitter.split(X_train,y_train))
    X_train,y_train,X_val,y_val = X_train[train_id],y_train[train_id],X_train[test_id],y_train[test_id]

    X_train = X_train[..., np.newaxis]
    X_test = X_test[..., np.newaxis]
    X_val = X_val[..., np.newaxis]

    INPUT_SHAPE = (X_train.shape[1], X_train.shape[2], 1)
    print(X_train[0].shape)
    print(X_train.shape)
    print(X_test.shape)


def build_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Conv2D(64,(3,3),activation="relu",input_shape=INPUT_SHAPE,kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D((3, 3), strides=(2,2), padding='same'))

    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
                                    kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D((3, 3), strides=(2,2), padding='same'))

    # 3rd conv layer
    model.add(tf.keras.layers.Conv2D(32, (2, 2), activation='relu',
                                    kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D((2, 2), strides=(2,2), padding='same'))

    # flatten output and feed into dense layer
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    tf.keras.layers.Dropout(0.3)

    # softmax output layer
    model.add(tf.keras.layers.Dense(10, activation='softmax'))

    return model

def test_model():
    pass

def main():
    model = build_model()
    model.compile(optimizer="Adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"])
    earlystop_callback = tf.keras.callbacks.EarlyStopping(monitor="accuracy", min_delta=0.001, patience=5)
    history = model.fit(X_train,y_train,epochs=30,batch_size=30,validation_data=(X_val,y_val),callbacks=[earlystop_callback])
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print("\nTest loss: {}, test accuracy: {}".format(test_loss, 100*test_acc))


if __name__=="__main__":
    main()