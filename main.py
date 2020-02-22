from io import BytesIO
from flask import Flask, request, send_file, render_template
from generate_labels import generate_labels, parse_data

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

    data = parse_data(text.split('\n'), indices)

    file_bytes = BytesIO(generate_labels(data, label_shape=shape))

    return send_file(file_bytes, attachment_filename='labels.pdf', as_attachment=True)

if __name__ == '__main__':
	app.run()
