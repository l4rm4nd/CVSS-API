from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from cvss import CVSS2, CVSS3, CVSS4
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Function to fix missing CVSS 4.0 Subsequent System Impact Metrics (SC, SI, SA)
def fix_cvss4_vector(vector):
    if "SC:" not in vector:
        vector += "/SC:N"
    if "SI:" not in vector:
        vector += "/SI:N"
    if "SA:" not in vector:
        vector += "/SA:N"
    return vector

@app.route('/cvss', methods=['GET'])
def calculate_cvss():
    vector = request.args.get('vector', '')
    version = os.getenv('VERSION', 'unknown')

    if not vector:
        return jsonify({"error": "No CVSS vector provided"}), 400

    try:
        if vector.startswith("CVSS:2."):
            score = CVSS2(vector).scores()[0]  # Base Score
        elif vector.startswith("CVSS:3."):
            score = CVSS3(vector).scores()[0]  # Base Score
        elif vector.startswith("CVSS:4."):
            vector = fix_cvss4_vector(vector) # Add SC/SI/SA if not provided
            score = CVSS4(vector).scores()[0]  # Base Score
        else:
            return jsonify({"error": "Unsupported or invalid CVSS vector string"}), 400

        return jsonify({"cvss_vector": vector, "cvss_score": score, "api_version": version})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
