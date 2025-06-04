from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from werkzeug.security import generate_password_hash, check_password_hash
from database.migration import Users, db,app, Transfers

@app.route('/')
def home():
    print("Rendering home.html")
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('register.html', error="Username and password are required."), 400

        existing_user = Users.query.filter_by(username=username).first()

        if existing_user:
            return render_template('register.html', error="User already exists. Please choose a different username."), 400
        
        hashed_password = generate_password_hash(password)
        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('login.html', error="Please enter both username and password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('transfer'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/transfer', methods=['GET','POST'])
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        sender_account = request.form.get('sender_account')
        receiver_account = request.form.get('receiver_account')
        receiver_bank = request.form.get('receiver_bank')
        receiver_name = request.form.get('receiver_name')
        amount = request.form.get('amount')
        currency = request.form.get('currency')
        description = request.form.get('description')
        frequency = request.form.get('frequency')

        if not all([sender_account, receiver_account, receiver_bank, receiver_name, amount, currency, frequency]):
            return render_template('transfer.html', error="All fields are required."),400
        
        try:
            amount = float(amount)
        except ValueError:
            return render_template('transfer.html', error="Invalid amount format."), 400
        
        new_transfer = Transfers(
            user_id=session['user_id'],
            sender_account=sender_account,
            receiver_bank=receiver_bank,
            receiver_account=receiver_account,
            receiver_name=receiver_name,
            amount=amount,
            currency=currency,
            description=description,
            frequency=frequency
        )
        db.session.add(new_transfer)
        db.session.commit()
        return redirect(url_for('success'))
    else:
        return render_template('transfer.html')


    

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)