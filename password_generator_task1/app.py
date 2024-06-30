# app.py
from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def generate_password(length=12, use_lowercase=True, use_uppercase=True, use_digits=True, use_punctuation=True):
    characters = ''
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_punctuation:
        characters += string.punctuation
    
    if not characters:
        raise ValueError("At least one character type should be selected.")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def calculate_strength(password):
    strength = 0
    categories = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation
    ]

    for category in categories:
        if any(char in category for char in password):
            strength += 1

    return strength

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    length = int(request.form.get('length', 12))
    use_lowercase = 'use_lowercase' in request.form
    use_uppercase = 'use_uppercase' in request.form
    use_digits = 'use_digits' in request.form
    use_punctuation = 'use_punctuation' in request.form

    try:
        password = generate_password(length, use_lowercase, use_uppercase, use_digits, use_punctuation)
        strength = calculate_strength(password)
    except ValueError as e:
        return render_template('index.html', error=str(e))

    return render_template('index.html', password=password, strength=strength)

if __name__ == '__main__':
    app.run(debug=True)
