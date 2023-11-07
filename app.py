from flask_cors import CORS
import logging
import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from main import store, search

UPLOAD_FOLDER = "./raw_files"
ALLOWED_EXTENSIONS = {'pdf'}  # {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level="INFO")

# Define a valid App-ID
valid_app_id = "30cf50c0-c4b9-4b5e-be09-f971c7a36d97"


def error_response(message, status_code):
    response = jsonify({"message": message})
    response.status_code = status_code
    return response


@app.before_request
def validate_app_id():
    if request.method != 'OPTIONS':
        if request.endpoint != 'static':
            app_id = request.headers.get('API-KEY')
            if app_id is None or app_id != valid_app_id:
                return error_response("Unauthorized", 401)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/file', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return error_response("No file", 400)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return error_response("No file", 400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        doc_name = store(path)
        return jsonify({"status": 0, "document": doc_name}), 201


@app.route('/answer', methods=['GET'])
def get_answer():
    phrase = request.args.get('phrase', type=str)
    document = request.args.get('document', type=str)
    answer = search(phrase, document)
    return jsonify({"answer": [{"page": 1, "phrase": phrase } for phrase in answer[0]]}), 200


if __name__ == '__main__':
    app.run(debug=True)
