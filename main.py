from io import BytesIO
from flask import Flask, request, send_file, render_template
from generate_labels import generate_labels

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/create', methods=['POST'])
def create():
    text = request.form['data']
    indices = [int(i.strip()) for i in request.form['indices'].split(',')]
    shape = request.form['shape'].split(',')
    shape = (int(shape[0].strip()), int(shape[1].strip()))

    data = []
    for l in text.split('\n'):
        words = l.split('\t')
        parts = [words[i].strip() for i in indices]
        data.append(parts)

    file_bytes = BytesIO(generate_labels(data, label_shape=shape))

    return send_file(file_bytes, attachment_filename='output.pdf', as_attachment=True)

if __name__ == '__main__':
	app.run()
