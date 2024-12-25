from flask import Flask, request, render_template
import os
from tinytag import TinyTag

app = Flask(__name__)

# Set upload folder
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_mp3_duration(mp3_file_path):
    tag = TinyTag.get(mp3_file_path)
    return tag.duration  # Duration in seconds

@app.route('/')
def index():
    return render_template('tryhtml.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Get the MP3 file duration
        duration = get_mp3_duration(filename)

        return render_template('tryhtml.html', duration=duration, filename=file.filename)
    
    return 'Invalid file type. Only MP3 is allowed.', 400

if __name__ == '__main__':
    app.run(debug=True)
