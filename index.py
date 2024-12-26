from flask import Flask, request, render_template
import os
from tinytag import TinyTag
import tempfile
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

def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file and allowed_file(file.filename):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            file.save(temp_file.name)

            # Get the MP3 file duration
            duration = get_mp3_duration(temp_file.name)

        return render_template('tryhtml.html', duration=duration, filename=file.filename)
    
    return 'Invalid file type. Only MP3 is allowed.', 400

if __name__ == '__main__':
    app.run(debug=True)
