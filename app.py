from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '79147326ccda4abffe36ebaf8b2be954cabd52f2'  

users = {'hamza': generate_password_hash('hamza')}  

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('calculator'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        stored_password = users.get(username)

        if stored_password and check_password_hash(stored_password, password):
            session['username'] = username
            return redirect(url_for('calculator'))
        else:
            return "Invalid username or password. Go back and try again."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if 'username' not in session:
        return redirect(url_for('login'))

    v = None
    percent_used = None

    if request.method == 'POST':
        try:
            X = float(request.form['Index X'])
            Y = float(request.form['Index Y'])
            mode = request.form['mode']

            percent = 54 if mode == 'Bullish Order Flow' else 39
            percent_used = percent
            t = percent / 100
            v = X + t * (Y - X)
        except ValueError:
            v = "Invalid input"

    return render_template('index.html', v=v, percent=percent_used)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)