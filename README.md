# MNIST-AUDIO-CLASSIFICATION

This is an audio version of MNIST dataset which contains audio samples of 10 labels (number from 0 to 9).

## Dataset

A simple audio/speech dataset consisting of recordings of spoken digits in wav files at 8kHz. The recordings are trimmed so that they have near minimal silence at the beginnings and ends.

[Link to Dataset](https://github.com/Jakobovski/free-spoken-digit-dataset)

**Sample Audio**

https://user-images.githubusercontent.com/36164059/129310445-8b9f8185-125f-431b-b7f4-380a0d3d36ef.mp4


## Demo
**yet to be built**


## Installation
Follow these instructions to make this project work in your own machine.


### Clone Repo
```bash
git clone https://github.com/Bot-Ro-Bot/MNIST-Audio-Classification.git
```

### Install Required Packages
```bash
cd MNIST-Audio-Classification
pip install -r requirements.txt
```

### Launch Program
```bash
python app.py
```

## Progress
* ~~Analyse Dataset~~
* ~~Process dataset (Feature extraction, normalization, train-test split)~~
* ~~Build Models~~
* ~~Test Models~~
* ~~Deploy Model~~


## So, How does it work?

### Model Development

**Data Extraction and Processing -> Feature Extraction -> Prepare Dataset -> Train Model -> Test Model -> Deploy Model**
 
### Client Request

**Client -> NGNIX Server -> uWSGI Server -> Flask -> End-Point (Model Inference) @ Tensorflow**


### Server Response

**Prediction -> Flask -> uWSGI Server -> NGNIX Server -> Client**

## Issues and Solution

* ### Port 80 Error
Start server.
```bash
docker-compose up
```
*Error Message*
```bash
Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use
``` 
See whats using port 80:
``` bash
 sudo netstat -pna | grep 80
```
Most probably, you have other server listening to port 80. Disable or remove them to make the port 80 free.

* ### Port 80 Error


## Acknowledgement
[Dataset](https://github.com/Jakobovski)

[Model](https://github.com/musikalkemist)
