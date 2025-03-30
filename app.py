from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os 
app = Flask(__name__)
CORS(app)  # Enable CORS for requests from any origin

# Load student data from CSV file
def load_student_data():
    students = []
    filepath=os.path.join(os.getcwd(),"q-fastapi.csv")
    try:
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append({
                    "studentId": int(row["studentId"]),
                    "class": row["class"]
                })
    except FileNotFoundError:
        print("The file 'students.csv' was not found.")
    return students

# Load the data once when the server starts
student_data = load_student_data()

@app.route("/api", methods=["GET"])
def get_students():
    """
    API endpoint to return student data.
    - If no class query parameter is specified, return all students.
    - If one or more class query parameters are specified, filter students by class.
    """
    # Get all query parameters for the 'class' filter
    class_filters = request.args.getlist("class")
    
    if not class_filters:
        # Return all students if no class filters are specified
        return jsonify({"students": student_data})
    
    # Filter students based on the class filters
    filtered_students = [
        student for student in student_data if student["class"] in class_filters
    ]
    return jsonify({"students": filtered_students})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
