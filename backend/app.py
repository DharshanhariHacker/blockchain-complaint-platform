from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Connect to your local blockchain (Ganache)
blockchain_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(blockchain_url))

# Import models
from models import User, Complaint

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        wallet_address = request.form['wallet_address']
        hashed_password = generate_password_hash(password)

        new_user = User(email=email, password_hash=hashed_password, wallet_address=wallet_address)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    complaints = Complaint.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, complaints=complaints)

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    complaint_data = request.form['complaint']
    new_complaint = Complaint(user_id=session['user_id'], complaint_data=complaint_data)
    db.session.add(new_complaint)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    complaints = Complaint.query.all()
    return render_template('admin_dashboard.html', complaints=complaints)

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)
