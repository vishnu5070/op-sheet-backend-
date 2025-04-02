from flask import Flask, render_template, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

app = Flask(__name__)

# Create a directory for PDFs if it doesn’t exist
if not os.path.exists("OP_Sheets"):
    os.makedirs("OP_Sheets")

# Disease-Doctor Mapping
disease_data = {
    "Fever": ("Dr. Rajesh Kumar", 101, "General Medicine"),
    "Diabetes": ("Dr. Sneha Sharma", 102, "Endocrinology"),
    "Heart Disease": ("Dr. Anil Mehta", 103, "Cardiology"),
    "Dermatology": ("Dr. Rina Das", 104, "Dermatology"),
    "General": ("Dr. Sandeep Rao", 105, "General Medicine")
}

# Route to render HTML page
@app.route("/")
def home():
    return render_template("index.html")

# Route to generate OP Sheet
@app.route("/generate_op", methods=["POST"])
def generate_op():
    data = request.json
    name, age, symptom = data["name"], data["age"], data["symptom"]
    
    if not name or not age or not symptom:
        return jsonify({"message": "All fields are required!"}), 400

    doctor, room, department = disease_data.get(symptom, ("Dr. Sandeep Rao", 105, "General Medicine"))
    filename = f"OP_Sheets/OP_Sheet_{name.replace(' ', '_')}.pdf"

    # Generate PDF
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Hospital OP Sheet")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Name: {name}")
    c.drawString(300, height - 90, f"Age: {age}")
    c.drawString(450, height - 90, f"Symptom: {symptom}")

    c.drawString(50, height - 120, f"Doctor Name: {doctor}")
    c.drawString(300, height - 120, f"Room No: {room}")
    c.drawString(450, height - 120, f"Dept: {department}")

    c.drawString(50, height - 150, f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    c.drawString(50, 50, "Doctor Signature: ___________________")
    c.save()

    return jsonify({"message": f"OP Sheet generated successfully: {filename}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
