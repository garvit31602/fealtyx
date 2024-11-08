from flask import Flask, jsonify, request, abort, render_template
import json
import requests

with open('students.json', 'r') as file:
    students = json.load(file)

app = Flask(__name__)

# In-memory data storage for students

# Helper function to find a student by ID
def find_student(student_id):
    return next((student for student in students if student["id"] == student_id), None)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

# Route to get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# Route to get a student by ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = find_student(student_id)
    if student is None:
        abort(404, description="Student not found")
    return jsonify(student)

# Helper function to save students data to students.json
def save_students():
    with open('students.json', 'w') as file:
        json.dump(students, file, indent=4)

# Update create_student to save data after adding a new student
@app.route('/students', methods=['POST'])
def create_student():
    if not request.json or not "name" in request.json or not "age" in request.json or not "email" in request.json:
        abort(400, description="Name, age, and email are required")
    new_student = {
        "id": students[-1]["id"] + 1 if students else 1,
        "name": request.json["name"],
        "age": request.json["age"],
        "email": request.json["email"]
    }
    students.append(new_student)
    save_students()  # Save data to file
    return jsonify(new_student), 201

# Update update_student to save data after modification
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = find_student(student_id)
    if student is None:
        abort(404, description="Student not found")
    if not request.json:
        abort(400, description="Request body is required")
    
    student["name"] = request.json.get("name", student["name"])
    student["age"] = request.json.get("age", student["age"])
    student["email"] = request.json.get("email", student["email"])
    save_students()  # Save data to file
    return jsonify(student)

# Update delete_student to save data after deletion
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = find_student(student_id)
    if student is None:
        abort(404, description="Student not found")
    students.remove(student)
    save_students()  # Save data to file
    return jsonify({"message": "Student deleted successfully"}), 200

# Endpoint to generate a summary for a student
@app.route('/students/summary', methods=['POST'])
def generate_summary():
    student_data = request.get_json()
    
    if not student_data:
        return jsonify({'error': 'Invalid data'}), 400
    
    student_name = student_data.get('name')
    student_age = student_data.get('age')
    student_email = student_data.get('email')
    
    if not student_name or not student_age or not student_email:
        return jsonify({'error': 'Missing student data'}), 400
    
    prompt = f"Generate a brief summary for the following student: Name: {student_name}, Age: {student_age}, Email: {student_email}. Provide a short description."

    ollama_url = 'http://localhost:11434/api/generate'  # Ensure this is correct
    data = {
        "model": "llama 3.2:1b",  # Correct model name, ensure there are no extra spaces
        "prompt": prompt,
        "stream":'false'
    }

    try:
        response = requests.post(ollama_url, json=data)
        response.raise_for_status()  # Raise exception for HTTP error responses
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return jsonify({'error': 'Failed to connect to Ollama'}), 500
    
    if response.status_code == 200:
        ollama_response = response.json()
        summary = ollama_response.get('choices', [{}])[0].get('text', 'No summary generated.')
        return jsonify({'summary': summary})
    else:
        print("Ollama error response:", response.json())  # Log the response for debugging
        return jsonify({'error': 'Failed to generate summary from Ollama'}), 500
    
@app.route('/chat', methods=['POST'])
def chat():
    data = {
        "model": "llama3.1:b",
        "prompt": "Why is the sky blue?",
        "stream": False
    }
    
    try:
        response = requests.post('http://localhost:11434/api/generate', json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return jsonify(response.text)  # Send the API response as JSON back to client
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return jsonify({'error': 'Failed to connect to Ollama'}), 500

if __name__ == '__main__':
    app.run(debug=True)

