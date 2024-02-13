from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Set up SQLite database
DB_FILE = 'site.db'

def initialize_database():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

initialize_database()

# Dummy user data (replace this with database queries in a real application)
def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_username(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = authenticate_user(username, password)
    if user:
        return redirect(url_for('dashboard', username=username))
    else:
        return render_template('index.html', error_message='Invalid username or password')

@app.route('/dashboard/<username>')
def dashboard(username):
    # Load food items from the database or another data source
    food_items = [
        {'name': 'Burger', 'price': 10, 'image': '/static/burger.jpg'},
        {'name': 'Pizza', 'price': 12, 'image': '/static/pizza.jpg'},
        {'name': 'Sushi', 'price': 15, 'image': '/static/sushi.jpg'},
        # Add more food items as needed
    ]
    return render_template('dashboard.html', username=username, food_items=food_items)

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']

        if get_user_by_username(username):
            return render_template('index.html', error_message='Username already exists. Please choose a different one.')
        else:
            create_user(username, password)
            return redirect(url_for('dashboard', username=username))  # Redirect to dashboard page after successful registration
    else:
        # Handle other request methods, such as GET
        return redirect(url_for('index'))  # Redirect to index page if method is not allowed

if __name__ == '__main__':
    app.run(debug=True)


