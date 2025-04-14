
from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import difflib
import io

app = Flask(__name__)

def extract_text(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image).strip()

def compare_texts(text1, text2):
    differ = difflib.Differ()
    result = list(differ.compare(text1.splitlines(), text2.splitlines()))
    return '\n'.join(result)

@app.route('/compare-labels', methods=['POST'])
def compare_labels():
    if 'master' not in request.files or 'submitted' not in request.files:
        return jsonify({'error': 'Please upload both files'}), 400

    master_file = request.files['master']
    submitted_file = request.files['submitted']

    master_text = extract_text(master_file)
    submitted_text = extract_text(submitted_file)

    differences = compare_texts(master_text, submitted_text)
    return jsonify({'differences': differences})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
