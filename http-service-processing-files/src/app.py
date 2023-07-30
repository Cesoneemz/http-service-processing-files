from flask import Flask, request, jsonify, render_template
from pathlib import Path
import pandas as pd
import os

app = Flask(__name__, template_folder='../templates')
UPLOAD_FOLDER = Path('http-service-processing-files', 'uploads')
print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('index.html', files=files)
    else:
        return jsonify({"error": "Invalid file format. Allowed formats: csv"}), 400


@app.route('/files', methods=['GET'])
def get_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files), 200


@app.route('/data', methods=['GET'])
def get_data():
    filename = request.args.get('filename')
    column = request.args.get('column')
    value = request.args.get('value')
    sort_by = request.args.get('sort_by')

    if not filename:
        return jsonify({"error": "Missing 'filename' parameter"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    df = pd.read_csv(filepath)


    if column and value:
        if column not in df.columns:
            return jsonify({"error": f"Column '{column}' not found in the file"}), 400
        col_dtype = df[column].dtype
        try:
            if col_dtype == 'int64' or col_dtype == 'float64':
                value = pd.to_numeric(value, errors='coerce')
            elif col_dtype == 'bool':
                value = bool(value)
            else:
                value = str(value)
        except:
            return jsonify({"error": f"Invalid value for column '{column}'"}), 400
        df = df[df[column] == value]

    if sort_by:
        if sort_by not in df.columns:
            return jsonify({"error": f"Column '{sort_by}' not found in the file"}), 400

        df = df.sort_values(by=sort_by)


    data = df.to_dict(orient='records')
    columns = df.columns.tolist()

    return render_template('sorted_data.html', filename=filename, columns=columns, data=data)


def main():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host="0.0.0.0")


if __name__ == '__main__':
   main()
