from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os

conn = "mongodb+srv://admin:mymdb$1234@hopeitdb.iczymzy.mongodb.net/?retryWrites=true&w=majority&appName=hopeitdb"
client = MongoClient(conn)
db = client.finanacedb
users = db.users

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        existing_user = users.find_one({'email': email})
        if existing_user:
            flash('該電子郵件已被註冊', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        users.insert_one({'name': name, 'email': email, 'password': hashed_password})
        flash('註冊成功,請登入', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = users.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            flash('登入成功', 'success')
            return redirect(url_for('index'))
        else:
            flash('登入失敗,請檢查您的電子郵件和密碼', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('您已成功登出', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
