from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            conversion_type = request.form['conversion_type']
            
            if conversion_type == 'sqm_to_tsubo':
                result = value / 3.30579  # 平方公尺轉坪
            elif conversion_type == 'tsubo_to_sqm':
                result = value * 3.30579  # 坪轉平方公尺
            
        except ValueError:
            error = "請輸入有效的數字"
    
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
