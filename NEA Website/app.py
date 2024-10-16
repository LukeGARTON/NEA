from flask import (
    Flask, render_template, request, redirect, url_for, session, abort, flash,
    jsonify, send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import join
import json
import os
import logging

app = Flask(__name__) #This initializes a flask web application instance

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testsite1.db'  #Here I am assigning the URL for the database connection

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #Setting a limit for the maximum file size of uploads
app.config['STATIC_FOLDER'] = 'static' #Specifies the folder where static files are stored

db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)

logging.basicConfig(level=logging.DEBUG)

# Fix logging reference to correct key
logging.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.route('/')
def index():
    return render_template('Index.html')
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    

    return render_template('signup.html')



@app.route('/login', methods=['POST']) #this route requires a check of the form i created on my index
def login():
    if request.method == 'POST':
        user_name = request.form.get('entered_username')
        pass_word = request.form.get('entered_password')
        
        user = Account.query.filter_by(username=user_name).first()
        
        if user and user.password == pass_word:
            session['username'] = user_name 
            return render_template('homepage.html', is_signed_in=True, user=user)
        else:
            return "Incorrect Username Or Password"
    
    return render_template(url_for('signup'))

@app.route('/savedetails', methods=['POST'])
def savedetails():
    if request.method == 'POST':
        try:
            print('Received form data:', request.form)
            print('Received files:', request.files)
            
            user_name = request.form.get('username') #telling the program that 
            pass_word = request.form.get('password')

            new_account = Account(
                username = user_name,
                password = pass_word,
            )
            db.session.add(new_account)
            db.session.commit()
            return jsonify({'message': 'New Account saved successfully.'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'An account with the same username already exists.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Method not allowed.'}), 405

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
