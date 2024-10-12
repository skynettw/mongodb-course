from flask import Flask

# 建立 Flask 應用程式
app = Flask(__name__)

# 定義路由和對應的處理函數
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
