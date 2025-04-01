from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple database to assign doctors based on symptoms
doctors = {
    "fever": "Dr. Smith (General Physician)",
    "chest pain": "Dr. Adams (Cardiologist)",
    "headache": "Dr. Brown (Neurologist)"
}

rooms = {
    "Dr. Smith (General Physician)": 101,
    "Dr. Adams (Cardiologist)": 102,
    "Dr. Brown (Neurologist)": 103
}

@app.route('/submit_patient', methods=['POST'])
def submit_patient():
    data = request.json
    name = data['name']
    age = data['age']
    symptoms = data['symptoms'].lower()
    
    # Assign doctor based on symptoms
    doctor = doctors.get(symptoms, "Dr. Johnson (General Practitioner)")  # Default if no match
    room = rooms.get(doctor, 100)  # Default room number if no match
    
    # Estimated wait time (dummy value for now)
    wait_time = "15-20 minutes"
    
    return jsonify({
        'doctor': doctor,
        'room': room,
        'wait_time': wait_time
    })

if __name__ == '__main__':
    app.run(debug=True)
