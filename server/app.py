from flask import Flask, jsonify, request
from GroqInitialize import initialize_groq_api
from FileUploader import handle_file_upload
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # Ensure UPLOAD_FOLDER is set

@app.route('/v1/test', methods=['GET'])
def test_end():
    return jsonify({
        'status': 'success',
        'message': 'Weapons Hot!'
    }), 200

@app.route('/v1/upload-csv-file', methods=['POST'])
def upload_files():
    if 'file' not in request.files:
        return jsonify({
            'status': 'fail',
            'message': 'No file part in the request'
        }), 400

    file = request.files['file']
    success, message, file_path = handle_file_upload(file, app.config['UPLOAD_FOLDER'])
    if not success:
        return jsonify({
            'status': 'fail',
            'message': message
        }), 400

    try:
        # Load the saved CSV file for processing (optional)
        data = pd.read_csv(file_path)
        return jsonify({
            'status': 'success',
            'message': message,
            'file_path': file_path,
            'data_preview': data.head().to_dict()  # Preview of the first 5 rows
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'fail',
            'message': 'Error processing file',
            'error': str(e)
        }), 500

@app.route('/v1/chat', methods=['POST'])
def chat_with_llm():
    return initialize_groq_api()

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=5000)