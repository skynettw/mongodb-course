from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import os
from datetime import datetime
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MongoDB連接
conn = "mongodb+srv://<account>:<password>@hopeitdb.iczymzy.mongodb.net/?retryWrites=true&w=majority&appName=hopeitdb"
client = MongoClient(conn)
db = client.finanacedb
users = db.users
categories = db.category
expenses = db.expense
incomes = db.income

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
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
    return redirect(url_for('login'))

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        amount = float(request.form['amount'])
        memo = request.form['memo']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        
        expenses.insert_one({
            'user': ObjectId(session['user_id']),
            'name': name,
            'category': category,
            'amount': amount,
            'memo': memo,
            'date': date
        })
        flash('支出已添加', 'success')
        return redirect(url_for('index'))
    
    user_categories = categories.find({'user': ObjectId(session['user_id'])})
    return render_template('add_expense.html', categories=user_categories)

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        amount = float(request.form['amount'])
        memo = request.form['memo']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        
        incomes.insert_one({
            'user': ObjectId(session['user_id']),
            'name': name,
            'category': category,
            'amount': amount,
            'memo': memo,
            'date': date
        })
        flash('收入已添加', 'success')
        return redirect(url_for('index'))
    
    user_categories = categories.find({'user': ObjectId(session['user_id'])})
    return render_template('add_income.html', categories=user_categories)

@app.route('/view_report')
def view_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    year = request.args.get('year')
    month = request.args.get('month')
    
    query = {'user': ObjectId(session['user_id'])}
    if year:
        query['date'] = {'$gte': datetime(int(year), 1, 1), '$lt': datetime(int(year)+1, 1, 1)}
    if month:
        if year:
            query['date'] = {'$gte': datetime(int(year), int(month), 1), '$lt': datetime(int(year), int(month)+1, 1)}
        else:
            current_year = datetime.now().year
            query['date'] = {'$gte': datetime(current_year, int(month), 1), '$lt': datetime(current_year, int(month)+1, 1)}
    
    user_expenses = list(expenses.find(query).sort('date', -1))
    user_incomes = list(incomes.find(query).sort('date', -1))
    
    all_years = sorted(set([expense['date'].year for expense in expenses.find({'user': ObjectId(session['user_id'])})] +
                           [income['date'].year for income in incomes.find({'user': ObjectId(session['user_id'])})]))
    
    return render_template('view_report.html', 
                           expenses=user_expenses, 
                           incomes=user_incomes, 
                           years=all_years,
                           selected_year=year,
                           selected_month=month)

@app.route('/edit_categories', methods=['GET', 'POST'])
def edit_categories():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        memo = request.form['memo']
        
        categories.insert_one({
            'user': ObjectId(session['user_id']),
            'name': name,
            'memo': memo
        })
        flash('類別已添加', 'success')
        return redirect(url_for('edit_categories'))
    
    user_categories = categories.find({'user': ObjectId(session['user_id'])})
    return render_template('edit_categories.html', categories=user_categories)

@app.route('/delete_category/<category_id>', methods=['POST'])
def delete_category(category_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 確保類別屬於當前用戶
    category = categories.find_one({'_id': ObjectId(category_id), 'user': ObjectId(session['user_id'])})
    if category:
        # 刪除類別
        categories.delete_one({'_id': ObjectId(category_id)})
        flash('類別已成功刪除', 'success')
    else:
        flash('無法刪除類別', 'danger')
    
    return redirect(url_for('edit_categories'))

@app.route('/delete_expense/<expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    expense = expenses.find_one({'_id': ObjectId(expense_id), 'user': ObjectId(session['user_id'])})
    if expense:
        expenses.delete_one({'_id': ObjectId(expense_id)})
        flash('支出已成功刪除', 'success')
    else:
        flash('無法刪除支出', 'danger')
    
    return redirect(url_for('view_report'))

@app.route('/delete_income/<income_id>', methods=['POST'])
def delete_income(income_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    income = incomes.find_one({'_id': ObjectId(income_id), 'user': ObjectId(session['user_id'])})
    if income:
        incomes.delete_one({'_id': ObjectId(income_id)})
        flash('收入已成功刪除', 'success')
    else:
        flash('無法刪除收入', 'danger')
    
    return redirect(url_for('view_report'))

@app.route('/statistics')
def view_statistics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = ObjectId(session['user_id'])
    
    # 獲取所有收入和支出
    all_expenses = list(expenses.find({'user': user_id}))
    all_incomes = list(incomes.find({'user': user_id}))
    
    # 合併收入和支出數據
    df_expenses = pd.DataFrame(all_expenses)
    df_incomes = pd.DataFrame(all_incomes)
    
    df_expenses['amount'] = -df_expenses['amount']  # 支出金額轉為負數
    df = pd.concat([df_expenses, df_incomes])
    
    # 轉換日期列
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['year_month'] = df['date'].dt.to_period('M')
    
    # 獲取年份列表
    years = sorted(df['year'].unique())
    
    # 獲取選擇的年份，預設為當前年份
    selected_year = request.args.get('year', datetime.now().year)
    selected_year = int(selected_year)
    
    # 獲取選擇的年月，預設為當前年月
    selected_year_month = request.args.get('year_month', datetime.now().strftime('%Y-%m'))
    
    # 按年月分組並計算總和
    monthly_sum = df[df['year'] == selected_year].groupby('year_month')['amount'].sum().reset_index()
    monthly_sum['year_month'] = monthly_sum['year_month'].astype(str)
    
    # 創建年度月份收支圖表
    trace = go.Bar(
        x=monthly_sum['year_month'],
        y=monthly_sum['amount'],
        marker=dict(
            color=['green' if x >= 0 else 'red' for x in monthly_sum['amount']]
        )
    )
    layout = go.Layout(title=f'{selected_year}年度月份收支統計')
    fig1 = go.Figure(data=[trace], layout=layout)
    graph1_json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 獲取選擇的月份數據
    df_selected_month = df[df['year_month'].astype(str) == selected_year_month]
    
    # 創建當月支出圓餅圖
    expenses_by_category = df_selected_month[df_selected_month['amount'] < 0].groupby('category')['amount'].sum().abs()
    fig2 = go.Figure(data=[go.Pie(labels=expenses_by_category.index, values=expenses_by_category.values)])
    fig2.update_layout(title=f'{selected_year_month} 支出類別統計')
    graph2_json = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 創建當月收入圓餅圖
    incomes_by_category = df_selected_month[df_selected_month['amount'] > 0].groupby('category')['amount'].sum()
    fig3 = go.Figure(data=[go.Pie(labels=incomes_by_category.index, values=incomes_by_category.values)])
    fig3.update_layout(title=f'{selected_year_month} 收入類別統計')
    graph3_json = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('statistics.html', 
                           graph1_json=graph1_json, 
                           graph2_json=graph2_json, 
                           graph3_json=graph3_json,
                           years=years,
                           selected_year=selected_year,
                           selected_year_month=selected_year_month)

if __name__ == '__main__':
    app.run(debug=True)