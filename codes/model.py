# importing necessary modules

from keras.models import save_model
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedShuffleSplit
import seaborn as sns
from sys import excepthook
from numpy.core.defchararray import encode

from config import *
import pickle

import warnings
warnings.filterwarnings("ignore")


# from tensorflow.keras.layers import Flatten, Conv2D, BatchNormalization, GlobalAveragePooling2D, MaxPool2D, Dense


def get_data(path=DATA_DIR):
    try:
        print("Fetching data ...")
        # data = pickle.load(open(os.path.join(path,"data.pickle"),"rb"))
        data = pickle.load(open(os.path.join(path, "data_new.pickle"), "rb"))
        print("Data Fetched- Successful")
    except Exception as ex:
        print("Data fetching failed due to: ", ex)
    return data["X"], data["Y"]


def process_data():
    X, Y = get_data()
    print("Shape of X: {} \nShape of Y: {}".format(X.shape, Y.shape))

    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(Y).astype('float64')
    Y = encoded_labels
    print("Label Encoding is as follows: ")
    mapping = dict(zip(encoder.classes_, range(len(encoder.classes_))))
    print(mapping)

    splitter = StratifiedShuffleSplit(
        n_splits=1, test_size=0.1, random_state=42)
    train_id, test_id = next(splitter.split(X, Y))
    X_train, y_train, X_test, y_test = X[train_id], Y[train_id], X[test_id], Y[test_id]

    train_id, test_id = next(splitter.split(X_train, y_train))
    X_train, y_train, X_val, y_val = X_train[train_id], y_train[train_id], X_train[test_id], y_train[test_id]

    X_train = X_train[..., np.newaxis]
    X_test = X_test[..., np.newaxis]
    X_val = X_val[..., np.newaxis]

    print(X_train[0].shape)
    print(X_train.shape)
    print(X_test.shape)

    return X_train, y_train, X_val, y_val, X_test, y_test


def build_model(INPUT_SHAPE):
    model = keras.models.Sequential()
    model.add(keras.layers.Conv2D(32, (3, 3), activation="relu",
              input_shape=INPUT_SHAPE, kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D(
        (3, 3), strides=(2, 2), padding='same'))

    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu',
                                     kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D(
        (3, 3), strides=(2, 2), padding='same'))

    # 3rd conv layer
    model.add(tf.keras.layers.Conv2D(128, (2, 2), activation='relu',
                                     kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D(
        (2, 2), strides=(2, 2), padding='same'))

    # flatten output and feed into dense layer
    model.add(tf.keras.layers.Flatten())

    model.add(tf.keras.layers.Dense(256, activation='relu'))
    tf.keras.layers.Dropout(0.3)

    model.add(tf.keras.layers.Dense(64, activation='relu'))
    tf.keras.layers.Dropout(0.3)

    # softmax output layer
    model.add(tf.keras.layers.Dense(10, activation='softmax'))

    print(model.summary())

    return model


def test_model():
    # save training curves

    # save confusion matrix

    # save 10 fold CV Box Plot
    pass


def main():
    # get data and process them
    X_train, y_train, X_val, y_val, X_test, y_test = process_data()
    INPUT_SHAPE = (X_train.shape[1], X_train.shape[2], 1)
    
    return

    # build a model
    model = build_model(INPUT_SHAPE)

    # compile model and run
    model.compile(optimizer="Adam",
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    earlystop_callback = tf.keras.callbacks.EarlyStopping(
        monitor="accuracy", min_delta=0.001, patience=5)
    history = model.fit(X_train, y_train, epochs=30, batch_size=30, validation_data=(
        X_val, y_val), callbacks=[earlystop_callback])

    # see performance of model on test data
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print("\nTest loss: {}, test accuracy: {}".format(test_loss, 100*test_acc))

    # save model
    try:
        print("Saving Model ...: ")
        save_model(model, os.path.join(MODEL_DIR, "model5.h5"))

    except Exception as ex:
        print("Saving Model failed due to: ", ex)


if __name__ == "__main__":
    main()
