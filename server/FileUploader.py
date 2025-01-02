import os
from werkzeug.utils import secure_filename

def handle_file_upload(file, upload_folder):
    """
    Handles the upload and saving of a file.

    :param file: The file to be saved.
    :param upload_folder: The folder where files will be saved.
    :return: A tuple with a success flag, message, and optional file path.
    """
    if not file:    
        return False, "No file provided", None

    if file.filename == '':
        return False, "No file selected", None

    try:
        # Ensure the upload folder exists
        os.makedirs(upload_folder, exist_ok=True)

        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return True, "File uploaded successfully", file_path
    except Exception as e:
        return False, f"Error saving file: {str(e)}", None