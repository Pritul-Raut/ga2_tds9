import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Load student marks from the external JSON file
def load_data():
    file_path = os.path.join(os.getcwd(), "q-vercel-python.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            if isinstance(data, list):  # If JSON is a list of objects
                # Convert list of objects into a dictionary
                return {item["name"]: item["marks"] for item in data}
            return data  # If it's already a dictionary
    except FileNotFoundError:
        print("File not found!")
        return {}
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")
        return {}

@app.route("/api", methods=["GET"])
def get_marks():
    # Load data from the JSON file
    student_marks = load_data()

    # Get the "name" query parameters from the request
    names = request.args.getlist("name")
    print("These are the names:", names)

    # Fetch marks for the provided names
    marks = [student_marks.get(name, 0) for name in names]  # Default to 0 if name not found
    return jsonify({"marks": marks})

if __name__ == "__main__":
    app.run()
