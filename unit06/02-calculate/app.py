from flask import Flask, render_template, request

app = Flask(__name__)

# 單位換算：1 坪 ≈ 3.305785 平方公尺
def sqm_to_ping(sqm):
    return sqm / 3.305785

def ping_to_sqm(ping):
    return ping * 3.305785

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if request.form['conversion_type'] == 'sqm_to_ping':
            sqm = float(request.form['value'])
            result = sqm_to_ping(sqm)
        elif request.form['conversion_type'] == 'ping_to_sqm':
            ping = float(request.form['value'])
            result = ping_to_sqm(ping)
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
