import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from web3storage import Web3Storage  # Correct import
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Set up database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Web3Storage with your API token
WEB3_STORAGE_API_KEY = os.getenv("WEB3_STORAGE_API_KEY")
web3_storage = Web3Storage(WEB3_STORAGE_API_KEY)  # Updated usage

# Define a simple complaint model
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    attachment_ipfs_hash = db.Column(db.String(200), nullable=True)

# Create database tables
with app.app_context():
    db.create_all()

# Endpoint to submit a complaint
@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    # Get data from request
    title = request.json.get('title')
    description = request.json.get('description')
    file = request.files.get('file')

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    # If a file is uploaded, store it on Web3.Storage
    attachment_ipfs_hash = None
    if file:
        # Upload file to Web3.Storage
        try:
            # Upload the file and get the IPFS hash
            ipfs_hash = web3_storage.upload(file)
            attachment_ipfs_hash = ipfs_hash
        except Exception as e:
            return jsonify({"error": f"File upload failed: {str(e)}"}), 500

    # Create a new complaint record in the database
    new_complaint = Complaint(title=title, description=description, attachment_ipfs_hash=attachment_ipfs_hash)
    db.session.add(new_complaint)
    db.session.commit()

    return jsonify({"message": "Complaint submitted successfully!", "complaint_id": new_complaint.id}), 201

# Endpoint to get all complaints
@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    complaints = Complaint.query.all()
    complaint_list = []

    for complaint in complaints:
        complaint_data = {
            "id": complaint.id,
            "title": complaint.title,
            "description": complaint.description,
            "attachment_ipfs_hash": complaint.attachment_ipfs_hash
        }
        complaint_list.append(complaint_data)

    return jsonify({"complaints": complaint_list}), 200

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
