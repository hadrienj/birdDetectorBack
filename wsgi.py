from flask import Flask, request, render_template, flash, redirect, url_for

app = Flask(__name__)


def is_allowed_file(filename):
    """ Checks if a filename's extension is acceptable """
    allowed_ext = filename.rsplit('.', 1)[1].lower() in ['wav']
    return '.' in filename and allowed_ext


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        if 'uploaded_file' not in request.files:
            flash('Please choose a file to upload')
            return redirect(request.url)

        audio_file = request.files['uploaded_file']

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
                    audio_file.save(filepath)
                    passed = True
                except Exception:
                    passed = False

                if passed:
                    return redirect(url_for('predict', filename=filename))
            else:
                flash('Choose a wav file.')
                return redirect(request.url)
        else:
            flash('An error occurred, try again.')
            return redirect(request.url)
