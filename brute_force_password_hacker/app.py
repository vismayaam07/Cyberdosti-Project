from flask import Flask, render_template, request, jsonify
import itertools
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack_password', methods=['POST'])
def crack_password():
    data = request.get_json()
    password = data.get('password')
    result = brute_force(password)
    return jsonify(result=result)

def brute_force(password):
    characters = string.ascii_letters + string.digits + string.punctuation
    attempts = 0

    for length in range(1, 9):
        for guess in itertools.product(characters, repeat=length):
            attempts += 1
            guess = ''.join(guess)
            if guess == password:
                return f"Password cracked: {guess} in {attempts} attempts"

    return "Password not cracked"

if __name__ == '__main__':
    app.run(debug=True)
