from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as fm

# 設置字體文件的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(current_dir, 'static', 'fonts', 'NotoSansCJKtc-Regular.otf')  # 使用 Noto Sans CJK TC 字體

# 創建字體屬性對象
font_prop = FontProperties(fname=font_path)

# 設置 matplotlib 使用自定義字體
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC'] + plt.rcParams['font.sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 為 session 設置密鑰

# 連接到MongoDB
client = MongoClient("mongodb+srv://<account>:<password>@hopeitdb.iczymzy.mongodb.net/?retryWrites=true&w=majority&appName=hopeitdb")
db = client.get_database("financedb")  # 假設我們使用名為"hopeitdb"的數據庫

@app.route('/')
def index():
    if 'username' in session:
        categories = db.category.find({"user": session['email']})
        expenses = db.expense.find({"user": session['email']})
        incomes = db.income.find({"user": session['email']})
        return render_template('index.html', username=session['username'], categories=categories, expenses=expenses, incomes=incomes)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if db.users.find_one({"email": email}):
            flash('電子郵件已被註冊', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        db.users.insert_one({"name": name, "email": email, "password": hashed_password})
        flash('註冊成功，請登入', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.users.find_one({"email": email})
        
        if user and check_password_hash(user['password'], password):
            session['username'] = user['name']
            session['email'] = user['email']
            flash('登入成功', 'success')
            return redirect(url_for('index'))
        flash('登入失敗，請檢查您的電子郵件和密碼', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    flash('您已成功登出', 'info')
    return redirect(url_for('index'))

@app.route('/add_item', methods=['POST'])
def add_item():
    if 'username' not in session:
        return redirect(url_for('login'))
    item_name = request.form.get('item_name')
    db.items.insert_one({"name": item_name, "user_email": session['email']})
    flash('項目已添加', 'success')
    return redirect(url_for('index'))

@app.route('/delete_item/<item_id>')
def delete_item(item_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    db.items.delete_one({"_id": ObjectId(item_id), "user_email": session['email']})
    flash('項目已刪除', 'success')
    return redirect(url_for('index'))

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        memo = request.form.get('memo')
        db.category.insert_one({"user": session['email'], "name": name, "memo": memo})
        flash('類別已添加', 'success')
        return redirect(url_for('index'))
    return render_template('add_category.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        memo = request.form.get('memo')
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        db.expense.insert_one({
            "user": session['email'],
            "name": name,
            "category": category,
            "amount": amount,
            "memo": memo,
            "date": date
        })
        flash('支出已添加', 'success')
        return redirect(url_for('index'))
    categories = db.category.find({"user": session['email']})
    return render_template('add_expense.html', categories=categories)

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        memo = request.form.get('memo')
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        db.income.insert_one({
            "user": session['email'],
            "name": name,
            "category": category,
            "amount": amount,
            "memo": memo,
            "date": date
        })
        flash('收入已添加', 'success')
        return redirect(url_for('index'))
    categories = db.category.find({"user": session['email']})
    return render_template('add_income.html', categories=categories)

@app.route('/edit_categories', methods=['GET', 'POST'])
def edit_categories():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        new_name = request.form.get('name')
        new_memo = request.form.get('memo')
        
        if category_id:
            db.category.update_one(
                {"_id": ObjectId(category_id), "user": session['email']},
                {"$set": {"name": new_name, "memo": new_memo}}
            )
            flash('類別已更新', 'success')
        else:
            db.category.insert_one({"user": session['email'], "name": new_name, "memo": new_memo})
            flash('新類別已添加', 'success')
        
        return redirect(url_for('edit_categories'))
    
    categories = db.category.find({"user": session['email']})
    return render_template('edit_categories.html', categories=categories)

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    db.category.delete_one({"_id": ObjectId(category_id), "user": session['email']})
    flash('類別已刪除', 'success')
    return redirect(url_for('edit_categories'))

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # 獲取年份和月份的篩選條件
    year = request.args.get('year', '')
    month = request.args.get('month', '')
    
    # 構建查詢條件
    query = {"user": session['email']}
    if year and month:
        start_date = datetime(int(year), int(month), 1)
        if int(month) == 12:
            end_date = datetime(int(year) + 1, 1, 1)
        else:
            end_date = datetime(int(year), int(month) + 1, 1)
        query['date'] = {'$gte': start_date, '$lt': end_date}
    elif year:
        start_date = datetime(int(year), 1, 1)
        end_date = datetime(int(year) + 1, 1, 1)
        query['date'] = {'$gte': start_date, '$lt': end_date}
    
    expenses = list(db.expense.find(query).sort("date", -1))
    incomes = list(db.income.find(query).sort("date", -1))
    
    # 將 ObjectId 轉換為字符串，並確保日期格式正確
    for expense in expenses:
        expense['_id'] = str(expense['_id'])
        if isinstance(expense['date'], datetime):
            expense['date'] = expense['date'].strftime('%Y-%m-%d')
    
    for income in incomes:
        income['_id'] = str(income['_id'])
        if isinstance(income['date'], datetime):
            income['date'] = income['date'].strftime('%Y-%m-%d')
    
    total_expense = sum(expense['amount'] for expense in expenses)
    total_income = sum(income['amount'] for income in incomes)
    balance = total_income - total_expense
    
    # 獲取所有可用的年份
    all_years = sorted(set([datetime.strptime(e['date'], '%Y-%m-%d').year for e in expenses + incomes]))
    
    return render_template('reports.html', 
                           expenses=expenses, 
                           incomes=incomes, 
                           total_expense=total_expense, 
                           total_income=total_income, 
                           balance=balance,
                           all_years=all_years,
                           selected_year=year,
                           selected_month=month)

@app.route('/delete_expense/<expense_id>')
def delete_expense(expense_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    db.expense.delete_one({"_id": ObjectId(expense_id), "user": session['email']})
    flash('支出已刪除', 'success')
    return redirect(url_for('reports'))

@app.route('/delete_income/<income_id>')
def delete_income(income_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    db.income.delete_one({"_id": ObjectId(income_id), "user": session['email']})
    flash('收入已刪除', 'success')
    return redirect(url_for('reports'))

@app.route('/statistics')
def statistics():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # 獲取用戶的所有收入和支出
    expenses = list(db.expense.find({"user": session['email']}))
    incomes = list(db.income.find({"user": session['email']}))
    
    # 獲取年份和月份的篩選條件
    selected_year = request.args.get('year', datetime.now().year)
    selected_month = request.args.get('month', datetime.now().strftime('%m'))
    
    # 生成年度月份收支統計圖
    yearly_stats = generate_yearly_stats(expenses, incomes, int(selected_year))
    
    # 生成當月類別支出和收入圓餅圖
    selected_date = f"{selected_year}-{selected_month}"
    expense_pie = generate_pie_chart(expenses, selected_date, 'expense')
    income_pie = generate_pie_chart(incomes, selected_date, 'income')
    
    # 獲取所有可用的年份
    all_years = sorted(set([expense['date'].year for expense in expenses] + [income['date'].year for income in incomes]))
    
    return render_template('statistics.html', 
                           yearly_stats=yearly_stats,
                           expense_pie=expense_pie,
                           income_pie=income_pie,
                           all_years=all_years,
                           selected_year=int(selected_year),
                           selected_month=int(selected_month))

def generate_yearly_stats(expenses, incomes, year):
    # 初始化每月收支統計
    monthly_stats = {f"{year}-{month:02d}": 0 for month in range(1, 13)}
    
    # 計算每月收支
    for expense in expenses:
        if expense['date'].year == year:
            date = expense['date'].strftime('%Y-%m')
            monthly_stats[date] -= expense['amount']
    
    for income in incomes:
        if income['date'].year == year:
            date = income['date'].strftime('%Y-%m')
            monthly_stats[date] += income['amount']
    
    # 生成圖表
    plt.figure(figsize=(12, 6))
    months = list(monthly_stats.keys())
    values = list(monthly_stats.values())
    colors = ['green' if v >= 0 else 'red' for v in values]
    plt.bar(months, values, color=colors)
    plt.title(f'{year}年每月收支餘額', fontproperties=font_prop)
    plt.xlabel('月份', fontproperties=font_prop)
    plt.ylabel('餘額', fontproperties=font_prop)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 將圖表轉換為 base64 編碼的字符串
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    return graphic

def generate_pie_chart(data, date, data_type):
    # 篩選指定年月的數據
    current_data = [item for item in data if item['date'].strftime('%Y-%m') == date]
    
    # 按類別統計金額
    category_totals = {}
    for item in current_data:
        category = item['category']
        amount = item['amount']
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    
    # 生成圓餅圖
    plt.figure(figsize=(8, 8))
    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
    title = f'{date} {data_type}類別統計'
    if data_type == 'expense':
        title = title.replace('expense', '支出')
    elif data_type == 'income':
        title = title.replace('income', '收入')
    plt.title(title, fontproperties=font_prop)
    
    # 將圖表轉換為 base64 編碼的字符串
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    return graphic

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)