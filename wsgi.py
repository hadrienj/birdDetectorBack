import os

from flask import Flask, request, flash, redirect
from flask_cors import CORS
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

from microfaune_package.microfaune.detection import RNNDetector

import json

import time
import numpy as np
import librosa
import base64

tf_config = tf.ConfigProto(
    intra_op_parallelism_threads=1,
    allow_soft_placement=True
)
sess = tf.Session(config=tf_config)
graph = tf.get_default_graph()


app = Flask(__name__)

cors = CORS(app)

# get env var
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']


def load_my_model():
    print("* Loading model...")
    global model
    print(model)

    model = RNNDetector('models/model_weights-20190919_220113.h5')


model = None
load_my_model()


def is_allowed_file(filename):
    """ Checks if a filename's extension is acceptable """
    allowed_ext = filename.rsplit('.', 1)[1].lower() in ['wav', 'mp3']
    return '.' in filename and allowed_ext


# def predict(filename):
#     filepath = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'], filename)

#     pred = model.predict_on_wav(filepath)
#     return pred


@app.route('/static/*', methods=['GET'])
def get_static():
    print('asdfasdfasdfasdfasdf')
    return 'ff'


def predict(X):
    """Predict bird presence on spectograms.

    Parameters
    ----------
    X: array-like
        List of features on which to run the model.

    Returns
    -------
    scores: array-like
        Prediction scores of the classifier on each audio signal
    local_scores: array-like
        Step-by-step  prediction scores for each audio signal
    """
    scores = []
    local_scores = []
    for x in X:
        print('ffff', x[np.newaxis, ...].shape)
        s, local_s = model.predict(x[np.newaxis, ...])
        scores.append(s[0])
        print(local_s)
        local_scores.append(np.array(local_s).flatten())
        print(local_scores)
    scores = np.array(s)
    return scores, local_scores



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return "Hello"

    if request.method == 'POST':
        print("================================================")
        t0 = time.time()
        # if 'file' not in request.files:
        #     flash('Please choose a file to upload')
        #     return redirect(request.url)

        # audio_file = request.files['file']
        audio_file = request.data

        # if audio_file.filename == '':
        #     flash('Please choose a file to upload')
        #     return redirect(request.url)

        if audio_file:
            print('a')
            if True:#is_allowed_file(audio_file.filename):
                print('alors')

                audio_val = np.array(list(json.loads(audio_file).values()))
                print('a', audio_val.shape)
                mel = audio_val.reshape(1, -1, 40, 1)
                mel = mel.astype(np.float32)
                mel = librosa.power_to_db(mel)
                np.save('mel', mel)
                # print('b', mel.shape)
                # print('test', mel[0, 1, 2, 0], mel[0, 3, 0, 0])

                # data_bytes = audio_file.read()
                # print(data_bytes)
                # mel = np.frombuffer(base64.b64decode(data_bytes), dtype=np.float32)
                # mel = mel.astype(np.float32)

                print('d mel', mel)

                # mel = librosa.feature.melspectrogram(S=mel, sr=48000, n_fft=2048,
                #                                      hop_length=1024, n_mels=40)

                # # mel = json.loads(audio_file)
                print('d mel', mel.shape)

                mel = mel.reshape(1, -1, 40, 1)
                # mel = mel.astype(np.float32)
                # mel = librosa.power_to_db(mel)

                with graph.as_default():
                    set_session(sess)
                    scores, local_scores = predict(np.array(mel))
                    print('e', time.time() - t0)
                return json.dumps(local_scores[0].tolist())

            else:
                flash('Choose a wav file.')
                return redirect(request.url)
        else:
            flash('An error occurred, try again.')
            return redirect(request.url)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    app.run()


