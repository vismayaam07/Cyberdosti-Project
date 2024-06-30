from flask import Flask, render_template, request, session, redirect, url_for, flash
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY').encode()

# Generate a Fernet key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        flash('Registration successful. Please login to continue.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if session.get('username') == username and session.get('password') == password:
            session['logged_in'] = True
            flash('Login successful.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if not session.get('logged_in'):
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))
    
    text = request.form['text']
    encrypted_text = cipher_suite.encrypt(text.encode()).decode()
    
    return render_template('index.html', encrypted_text=encrypted_text)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if not session.get('logged_in'):
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))
    
    encrypted_text = request.form['encrypted_text']
    decrypted_text = cipher_suite.decrypt(encrypted_text.encode()).decode()
    
    return render_template('index.html', decrypted_text=decrypted_text)

if __name__ == '__main__':
    app.run(debug=True)
