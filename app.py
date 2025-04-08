from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import uuid
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='.', static_url_path='')

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return app.send_static_file("index.html")  # ✅ Serves index.html from root

@app.route("/generate", methods=["POST"])
def generate():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(str(uuid.uuid4()) + "_" + file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Clean previous outputs
        for f in os.listdir(OUTPUT_FOLDER):
            os.remove(os.path.join(OUTPUT_FOLDER, f))

        # Run image processing
        result = subprocess.run(
            ['python', 'run_examples.py', filepath, OUTPUT_FOLDER],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                "error": "Error generating images",
                "stdout": result.stdout,
                "stderr": result.stderr
            }), 500

        output_files = sorted(os.listdir(OUTPUT_FOLDER))
        return jsonify({"output_images": output_files})

    return jsonify({"error": "Invalid file format"}), 400

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
