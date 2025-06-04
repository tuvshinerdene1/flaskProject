from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'flask-db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Bad Request: Missing username or password in the form data", 400

        # Check if the username already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            return "User already exists. Please choose a different username.", 400
        
        # If not, insert the new user
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))  # Redirect to login page after registration
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check for missing input
        if not username or not password:
            return render_template('login.html', error="Please enter both username and password")

        # Validate credentials
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()  # Fetch user record if it exists
        cur.close()

        if user:
            # Login successful, redirect to another page
            return redirect(url_for('question'))
        else:
            # Invalid credentials, show error
            return render_template('login.html', error="Invalid username or password")

    # If GET request, render login form
    return render_template('login.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        question_text = request.form.get('question')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO questions (question) VALUES (%s)", (question_text,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('success'))  
    else:
        return render_template('question.html')
    

@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)