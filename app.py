from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files')
    for file in uploaded_files:
        if file and file.filename.endswith('.html'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('calculate_pagerank'))

@app.route('/pagerank')
def calculate_pagerank():
    from pagerank import build_graph_and_rank
    result = build_graph_and_rank(app.config['UPLOAD_FOLDER'])
    return render_template('result.html', pagerank=result)

if __name__ == '__main__':
    app.run(debug=True)