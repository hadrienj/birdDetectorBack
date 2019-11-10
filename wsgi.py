import os

from flask import Flask, request, flash, redirect
from flask_cors import CORS
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

from microfaune_package.microfaune.detection import RNNDetector

import json

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
    allowed_ext = filename.rsplit('.', 1)[1].lower() in ['wav']
    return '.' in filename and allowed_ext


# def predict(filename):
#     filepath = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'], filename)

#     pred = model.predict_on_wav(filepath)
#     return pred


@app.route('/static/*', methods=['GET'])
def get_static():
    print('asdfasdfasdfasdfasdf')
    return 'ff'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return "Hello"

    if request.method == 'POST':
        print("================================================")
        if 'file' not in request.files:
            flash('Please choose a file to upload')
            return redirect(request.url)

        audio_file = request.files['file']

        if audio_file.filename == '':
            flash('Please choose a file to upload')
            return redirect(request.url)

        if audio_file:
            if is_allowed_file(audio_file.filename):
                passed = False
                try:
                    filename = audio_file.filename
                    filepath = os.path.join(os.path.dirname(__file__),
                                            app.config['UPLOAD_FOLDER'], filename)
                    print(f'An audio file has been sent. Saving {filepath} ...')
                    audio_file.save(filepath)
                    passed = True
                except Exception:
                    passed = False

                if passed:
                    filepath = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'], filename)
                    print("===", filepath)

                    with graph.as_default():
                        set_session(sess)
                        pred = model.predict_on_wav(filepath)
                        print('pred', pred)
                    return json.dumps(pred[1].tolist())
                    # return redirect(url_for('predict', filename=filename))
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
